use headless_chrome::{Browser, LaunchOptionsBuilder};
use pyo3::exceptions::{PyIndexError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyTuple};
use rand::Rng;
use reqwest::blocking::Client;
use scraper::{Html, Selector};
use std::cell::RefCell;
use std::collections::HashMap;

#[pyclass]
#[derive(Clone)]
struct Fetch {
    url: String,
    html: RefCell<String>,
    queries: RefCell<Vec<QueryInfo>>,
    data: RefCell<Option<PyObject>>,
}

#[derive(Clone)]
struct QueryInfo {
    selector: String,
    key: Option<String>,
    extraction: Option<Py<PyAny>>,
    limit: Option<usize>,
}

#[pymethods]
impl Fetch {
    #[new]
    fn new(url: String) -> PyResult<Self> {
        let client = Client::builder()
            .user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            .build()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;

        let response = client
            .get(&url)
            .send()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;

        let html = response
            .text()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;

        Ok(Fetch {
            url,
            html: RefCell::new(html),
            queries: RefCell::new(Vec::new()),
            data: RefCell::new(None),
        })
    }

    fn query(slf: PyRef<Self>, selector: String, key: Option<String>) -> PyResult<Py<Self>> {
        slf.queries.borrow_mut().push(QueryInfo {
            selector,
            key,
            extraction: None,
            limit: None,
        });
        Py::new(slf.py(), slf.clone())
    }

    fn extract(slf: PyRef<Self>, extraction: &PyDict) -> PyResult<Py<Self>> {
        if let Some(last_query) = slf.queries.borrow_mut().last_mut() {
            last_query.extraction = Some(extraction.to_object(slf.py()));
        }
        Py::new(slf.py(), slf.clone())
    }

    fn limit(slf: PyRef<Self>, limit: usize) -> PyResult<Py<Self>> {
        if let Some(last_query) = slf.queries.borrow_mut().last_mut() {
            last_query.limit = Some(limit);
        }
        Py::new(slf.py(), slf.clone())
    }

    fn get_data<'py>(&self, py: Python<'py>) -> PyResult<PyObject> {
        if self.data.borrow().is_none() {
            let mut final_results = self.scrape_data(py)?;

            // If the results are empty, try headless browsing
            if final_results.is_empty() {
                final_results = self.headless_scrape(py)?;
            }

            let py_final_result = if final_results.len() == 1 {
                final_results[0].clone()
            } else {
                PyList::new(py, &final_results).into()
            };

            *self.data.borrow_mut() = Some(py_final_result);
        }

        Ok(self.data.borrow().as_ref().unwrap().clone_ref(py))
    }

    fn scrape_data<'py>(&self, py: Python<'py>) -> PyResult<Vec<PyObject>> {
        let document = Html::parse_document(&self.html.borrow());
        let mut keyed_results: HashMap<String, Vec<PyObject>> = HashMap::new();
        let mut unkeyed_results: Vec<PyObject> = Vec::new();
        let mut key_limits: HashMap<String, Option<usize>> = HashMap::new();

        for query_info in self.queries.borrow().iter() {
            let selector = Selector::parse(&query_info.selector)
                .map_err(|e| PyErr::new::<PyValueError, _>(format!("Invalid selector: {:?}", e)))?;
            let extraction = query_info.extraction.as_ref().map(|e| e.as_ref(py));

            let mut query_result = Vec::new();
            for element in document.select(&selector) {
                if let Some(extraction_dict) = extraction {
                    let item = extract_data(py, element, extraction_dict.downcast()?)?;
                    query_result.push(item.to_object(py));
                }
            }

            if let Some(key) = &query_info.key {
                keyed_results
                    .entry(key.clone())
                    .or_insert_with(Vec::new)
                    .push(PyList::new(py, &query_result).into());
                if let Some(limit) = query_info.limit {
                    key_limits
                        .entry(key.clone())
                        .and_modify(|e| *e = Some((*e).unwrap_or(usize::MAX).min(limit)))
                        .or_insert(Some(limit));
                }
            } else {
                if let Some(limit) = query_info.limit {
                    query_result.truncate(limit);
                }
                unkeyed_results.push(PyList::new(py, &query_result).into());
            }
        }

        let mut final_results = Vec::new();

        // Handle unkeyed results
        final_results.extend(unkeyed_results);

        // Handle keyed results
        for (key, results) in keyed_results {
            let limit = key_limits.get(&key).and_then(|&l| l).unwrap_or(usize::MAX);
            let merged = merge_keyed_results(py, &results, limit)?;
            final_results.push(merged.into());
        }

        // Remove any empty lists
        final_results.retain(|r| {
            let list: &PyList = r.downcast(py).unwrap();
            !list.is_empty()
        });

        Ok(final_results)
    }

    fn headless_scrape<'py>(&self, py: Python<'py>) -> PyResult<Vec<PyObject>> {
        let mut rng = rand::thread_rng();

        let options = LaunchOptionsBuilder::default()
            .headless(true)
            .sandbox(false)
            .window_size(Some((1920, 1080)))
            .build()
            .map_err(|e| {
                PyErr::new::<PyValueError, _>(format!("Failed to build launch options: {:?}", e))
            })?;

        let browser = Browser::new(options).map_err(|e| {
            PyErr::new::<PyValueError, _>(format!("Failed to launch browser: {:?}", e))
        })?;

        let tab = browser.new_tab().map_err(|e| {
            PyErr::new::<PyValueError, _>(format!("Failed to create new tab: {:?}", e))
        })?;

        // Set a random user agent
        let user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        ];
        let user_agent = user_agents[rng.gen_range(0..user_agents.len())];
        tab.set_user_agent(user_agent, None, None).map_err(|e| {
            PyErr::new::<PyValueError, _>(format!("Failed to set user agent: {:?}", e))
        })?;

        // Navigate to the URL
        tab.navigate_to(&self.url).map_err(|e| {
            PyErr::new::<PyValueError, _>(format!("Failed to navigate to URL: {:?}", e))
        })?;

        // Wait for the page to load
        tab.wait_for_element("body").map_err(|e| {
            PyErr::new::<PyValueError, _>(format!("Failed to wait for body: {:?}", e))
        })?;

        // Wait for 10 seconds to see if the query becomes available
        let start_time = std::time::Instant::now();
        let timeout = std::time::Duration::from_secs(10);
        while start_time.elapsed() < timeout {
            if let Ok(_) = tab.wait_for_element(&self.queries.borrow()[0].selector) {
                break;
            }
            std::thread::sleep(std::time::Duration::from_millis(100));
        }

        // Get the page content
        let content = tab.get_content().map_err(|e| {
            PyErr::new::<PyValueError, _>(format!("Failed to get page content: {:?}", e))
        })?;

        // Update the HTML content
        *self.html.borrow_mut() = content;

        // Re-run the scraping logic with the new content
        self.scrape_data(py)
    }

    fn __getitem__(&self, py: Python, index: isize) -> PyResult<PyObject> {
        let data = self.get_data(py)?;
        let outer_list: &PyList = data.downcast(py)?;
        let outer_len = outer_list.len() as isize;

        // Adjust index for negative values
        let adjusted_index = if index < 0 { outer_len + index } else { index };

        if adjusted_index < 0 || adjusted_index >= outer_len {
            return Err(PyIndexError::new_err("list index out of range"));
        }

        let item = outer_list.get_item(adjusted_index as usize)?;

        // Check if the item is a list and handle the Result properly
        if item.is_instance_of::<PyList>()? {
            Ok(item.to_object(py))
        } else {
            // If it's not a list, wrap it in a list for consistency
            Ok(PyList::new(py, &[item]).to_object(py))
        }
    }

    fn count(&self, py: Python) -> PyResult<usize> {
        let data = self.get_data(py)?;
        let outer_list: &PyList = data.downcast(py)?;

        let mut total_count = 0;
        for item in outer_list.iter() {
            if let Ok(inner_list) = item.downcast::<PyList>() {
                total_count += inner_list.len();
            } else {
                // If it's not a list, count it as a single item
                total_count += 1;
            }
        }

        Ok(total_count)
    }

    fn __str__(&self, py: Python) -> PyResult<String> {
        let data = self.get_data(py)?;
        Ok(data.to_string())
    }

    fn __repr__(&self, py: Python) -> PyResult<String> {
        let data = self.get_data(py)?;
        Ok(format!("Fetch(data={})", data))
    }

    fn __len__(&self, py: Python) -> PyResult<usize> {
        self.count(py)
    }
}

fn extract_data<'py>(
    py: Python<'py>,
    element: scraper::ElementRef<'_>,
    extraction_dict: &'py PyDict,
) -> PyResult<&'py PyDict> {
    let item = PyDict::new(py);
    for (key, value) in extraction_dict.iter() {
        let extracted_value = match value.extract::<String>() {
            Ok(selector_str) => {
                if selector_str == "." {
                    element.text().collect::<String>().to_object(py)
                } else if selector_str.contains('@') {
                    let parts: Vec<&str> = selector_str.split('@').collect();
                    let (selector_part, attr_name) = (parts[0], parts[1]);
                    let selector = Selector::parse(selector_part).map_err(|e| {
                        PyErr::new::<PyValueError, _>(format!("Invalid selector: {:?}", e))
                    })?;
                    element
                        .select(&selector)
                        .next()
                        .and_then(|el| el.value().attr(attr_name))
                        .unwrap_or("")
                        .to_object(py)
                } else {
                    let selector = Selector::parse(&selector_str).map_err(|e| {
                        PyErr::new::<PyValueError, _>(format!("Invalid selector: {:?}", e))
                    })?;
                    element
                        .select(&selector)
                        .next()
                        .map(|el| el.text().collect::<String>())
                        .unwrap_or_default()
                        .to_object(py)
                }
            }
            Err(_) => {
                let callable = value.extract::<PyObject>()?;
                let args = PyTuple::new(py, &[element.html().to_object(py)]);
                callable.call1(py, args)?
            }
        };
        item.set_item(key, extracted_value)?;
    }
    Ok(item)
}

fn merge_keyed_results(py: Python, results: &[PyObject], limit: usize) -> PyResult<Py<PyList>> {
    let merged = PyList::empty(py);
    let mut merged_dicts: Vec<Py<PyDict>> = Vec::new();

    // First, collect all dictionaries from all results
    for result_list in results.iter().rev() {
        // Reverse the iteration order
        let list: &PyList = result_list.downcast(py)?;
        for (i, item) in list.iter().enumerate() {
            if i >= limit {
                break;
            }
            let dict: &PyDict = item.downcast()?;
            if i >= merged_dicts.len() {
                merged_dicts.push(dict.copy()?.into_py(py));
            } else {
                let existing = merged_dicts[i].as_ref(py);
                let updated = existing.copy()?;
                for (k, v) in dict.iter() {
                    updated.set_item(k, v)?;
                }
                merged_dicts[i] = updated.into_py(py);
            }
        }
    }

    // Then, add the merged dictionaries to the result list
    for dict in merged_dicts {
        merged.append(dict)?;
    }

    Ok(merged.into())
}

#[pymodule]
fn trywebscraping(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Fetch>()?;
    Ok(())
}
