let previousViewLink = document.querySelector(".previous-view.view-child");
let nextViewLink = document.querySelector(".next-to-view.view-child");
let orderPageStorageKey = "order_pages";

function initialzePagesText() {
  let order = getObjectFromLocalStorageByKey(paginationOrderPageKey);
  console.log("initialzePagesText", order);

  if (order) {
    let presentNum = order[paginationCurrPageKey];
    let grossNum = order[paginationTotalPageKey];

    console.log("presentNum", presentNum, "grossNum", grossNum);
    grossIdSpan.textContent = grossNum;
    presentIdSpan.textContent = presentNum;
  }
}

function previousViewPage() {
  // 为元素添加点击事件监听器
  previousViewLink.addEventListener("click", function (event) {
    event.preventDefault(); // 阻止链接默认行为（如果需要）
    clearElementsByClassName(paginationInfoTagCls);
    unsetTriggerChecked();

    let order = getObjectFromLocalStorageByKey(paginationOrderPageKey);
    let currOrder = order[paginationCurrPageKey];

    if (currOrder != undefined || currOrder != null || currOrder != "") {
      currOrder -= 1;
      if (currOrder > 0) {
        destinationByOrder(paginationTokenKey, currOrder);
      } else {
        feedTxtIntoTag("Already First Page");
      }
    }
  });
}

function nextViewPage() {
  // 为元素添加点击事件监听器
  nextViewLink.addEventListener("click", function (event) {
    event.preventDefault(); // 阻止链接默认行为（如果需要）
    clearElementsByClassName(paginationInfoTagCls);
    unsetTriggerChecked();

    let order = getObjectFromLocalStorageByKey(paginationOrderPageKey);
    let currOrder = order[paginationCurrPageKey];

    if (currOrder != undefined || currOrder != null || currOrder != "") {
      currOrder += 1;
      console.log("nextViewPage.currOrder", currOrder);

      let checkSign = checkCurrAndTotalNum(currOrder);
      if (checkSign) {
        destinationByOrder(paginationTokenKey, currOrder);
      }
    }
  });
}

function destinationByOrder(tokenKey, destPosition) {
  clearElementsByClassName(paginationInfoTagCls);
  unsetTriggerChecked();

  let header = getLocalToken(tokenKey);
  if (header == false) {
    let msg = "Account status is abnormal, please sign in again";
    feedTxtIntoTag(msg);
    return;
  }

  let titleObj = checkTitleParam(titleStringKey);
  if (titleObj == null) {
    let pageOrder = { page_order: destPosition };
    navigationSent(paginationRequestUrl, pageOrder, header);
  } else {
    collectsParameter(
      paginationTokenKey,
      titleObj.search_condition,
      destPosition
    );
  }
}

function checkTitleParam(tokenKey) {
  let titleStr = localStorage.getItem(tokenKey);
  if (titleStr != "" || titleStr != undefined || titleStr != null) {
    let titleObj = JSON.parse(titleStr);
    console.log("titleObj", titleObj);
    return titleObj;
  }
  return null;
}

function navigationSent(requestUrl, parameters, header) {
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
      navigationSentTackle(data, parameters);
      return data;
    })
    .then(function (data) {
      if (data.state != 200) {
        feedTxtIntoTag(data.message);
      }
      return data;
    })
    .then(function (data) {
      if (data.state != 200) {
        updateCurrPage(parameters.page_order);
      }
      return data;
    })
    .then(function (data) {
      if (data.state != 200) {
        clearElementsByClassName(exhibitionTabulationTag);
      }
    })
    .then(function () {
      initialzePagesText();
    })
    .catch((error) => {
      console.error(error);
    });
}

function navigationSentTackle(params) {
  if (params.state == 200) {
    console.log("navigationSentTackle", params.pagination);
    let pageMark = {
      current_page: params.pagination[paginationCurrPageKey],
      total_pages: params.pagination[paginationTotalPageKey],
    };
    setToObjectLocalStorage(paginationOrderPageKey, pageMark);

    appendInsertEle(exhibitionTabulationTag, params.pagination.paged_data);
  }
}

function clearElementsByClassName(className) {
  // 获取所有具有指定类名的元素
  let elements = document.getElementsByClassName(className);
  // 遍历这些元素并清空它们的内容和子元素
  for (let i = 0; i < elements.length; i++) {
    elements[i].innerHTML = "";
  }
}

function handleEntryEnterKey(event) {
  if (event.keyCode === 13) {
    const inputElement = event.target;
    const inputValue = parseInt(inputElement.value, 10);
    if (inputValue) {
      destinationByOrder(paginationTokenKey, inputValue);
    }
  }
}

function getInputJumpValue() {
  const inputElement = document.querySelector(".position-jump");
  const inputValue = inputElement.value;
  if (inputValue) {
    destinationByOrder(paginationTokenKey, Number(inputValue));
  }
}

function updateCurrPage(page_order) {
  let orderObj = getObjectFromLocalStorageByKey(paginationOrderPageKey);
  console.log("orderObj", orderObj);
  orderObj[paginationCurrPageKey] = page_order;

  localStorage.removeItem(paginationOrderPageKey);
  setToObjectLocalStorage(paginationOrderPageKey, orderObj);
}

let checkCurrAndTotalNum = (currOrder) => {
  let pageNumObj = JSON.parse(localStorage.getItem(orderPageStorageKey));
  console.log("pageNumObj", pageNumObj);

  if (currOrder > pageNumObj.total_pages) {
    feedTxtIntoTag("Already last page");
    return false;
  }
  return true;
};

let unsetTriggerChecked = () => {
  if (triggerBoxElement.checked) {
    triggerBoxElement.checked = false;
  }
};
