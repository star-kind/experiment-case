let titleRequestUrl = "essay-search-title";
let titleStringKey = "title_remark";
let grossIdSpan = document.querySelector("#gross-id-number");
let presentIdSpan = document.querySelector("#present-id-number");

function getInputTitleStringValue() {
  const inputElement = document.querySelector(".position-search");
  const inputValue = inputElement.value.trim();
  if (inputValue) {
    console.info("getInputTitleStringValue", inputValue);
    collectsParameter(paginationTokenKey, inputValue, null);
  }
}

function handleSearchingTitleEnterKey(event) {
  if (event.keyCode === 13) {
    const inputElement = event.target;
    const inputValue = inputElement.value;
    if (inputValue) {
      console.log("handleSearchingTitleEnterKey", inputValue);
      collectsParameter(paginationTokenKey, inputValue, null);
    }
  }
}

function collectsParameter(tokenKey, stringValue, pageNum) {
  let header = getLocalToken(tokenKey);
  let parameters = { title: stringValue };

  if (pageNum == null) {
    parameters.page_order = 1;
  } else {
    parameters.page_order = pageNum;
  }

  getListByTitleUrl(titleRequestUrl, parameters, header);
}

function getListByTitleUrl(requestUrl, parameters, header) {
  fetch(requestUrl, {
    method: "POST",
    body: JSON.stringify(parameters),
    cache: "no-cache", // 对应于false
    headers: header,
    contentType: "application/json",
  })
    .then((response) => {
      console.log(response);
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Error: ", response.statusText);
      }
    })
    .then(function (data) {
      console.log(data);
      if (data.state == 200 && data.pagination.paged_data.length != 0) {
        appendInsertEle(exhibitionTabulationTag, data.pagination.paged_data);
      }
      return data;
    })
    .then((data) => {
      if (data.state == 200 && data.pagination.paged_data.length == 0) {
        clearElementsByClassName(exhibitionTabulationTag);
      }
      return data;
    })
    .then((data) => {
      if (data.state == 200 && data.pagination.paged_data.length == 0) {
        grossIdSpan.textContent = 0;
        presentIdSpan.textContent = 0;
      }
      return data;
    })
    .then(function (params) {
      updatePagesRemark(params);
      return params;
    })
    .then(function (data) {
      if (data.state != 200) {
        clearElementsByClassName(exhibitionTabulationTag);
      }
    })
    .then(() => {
      setToObjectLocalStorage(titleStringKey, {
        search_condition: parameters.title,
      });
    })
    .then(initialzePagesText)
    .catch((error) => {
      console.error(error);
    });
}

function updatePagesRemark(params) {
  let pageMark = {
    current_page: params.pagination[paginationCurrPageKey],
    total_pages: params.pagination[paginationTotalPageKey],
  };
  setToObjectLocalStorage(paginationOrderPageKey, pageMark);
}
