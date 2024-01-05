let paginationRequestUrl = "essay-blogs-tabulation";
let paginationInfoTagCls = "hint-exhibition-element";
let paginationTokenKey = "token";
let paginationDelay = 8;
let paginationUsrnameEle = "mail-item";
let paginationUsernameCookie = "account_stamp";
let exhibitionTabulationTag = "exhibition-tabulation-div";
let paginationCurrPageKey = "current_page";
let paginationTotalPageKey = "total_pages";
let paginationOrderPageKey = "order_pages";
let cellDivideNameId = "cell-container-";
const informationTag = document.querySelector("#id-hint-feedback-element");

window.onload = function () {
  initExhibitUsrname(paginationUsrnameEle, paginationUsernameCookie);
  initialExecuted(paginationTokenKey);
  previousViewPage();
  nextViewPage();
  initialzePagesText();
};

function initExhibitUsrname(eleSelector, cookieName) {
  let eles = document.getElementsByClassName(eleSelector);
  let val = getCookie(cookieName);

  for (let i = 0; i < eles.length; i++) {
    eles[i].textContent = val;
  }
}

function initialExecuted(tokenKey) {
  let header = getLocalToken(tokenKey);
  let pageOrder = gainPageOrderNum();
  let titleObject = getTitleValueObj();

  if (titleObject) {
    let requestParameter = {
      title: titleObject.search_condition,
      page_order: pageOrder.page_order,
    };
    handle2Send(titleRequestUrl, requestParameter, header);
  } else {
    handle2Send(paginationRequestUrl, pageOrder, header);
  }
}

let getTitleValueObj = () => {
  let titleValueObj = getObjectFromLocalStorageByKey(titleStringKey);
  if (titleValueObj) {
    console.log("titleValueObj", titleValueObj);
    return titleValueObj;
  }
  return null;
};

let gainPageOrderNum = () => {
  let pageOrder = {};
  let order = getObjectFromLocalStorageByKey(paginationOrderPageKey);
  console.log("order", order);

  if (isEmptyObject(order) == true || order == null) {
    pageOrder.page_order = 1;
  } else {
    pageOrder.page_order = order[paginationCurrPageKey];
  }

  console.log("pageOrder", pageOrder);
  return pageOrder;
};

function handle2Send(requestUrl, data, header) {
  fetch(requestUrl, {
    method: "POST",
    body: JSON.stringify(data),
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
      tackle(data);
      return data;
    })
    .then(function (data) {
      if (data.state != 200) {
        feedTxtIntoTag(data.message);
        setTimeout(() => {
          informationTag.textContent = "";
        }, 6 * 1000);
      }
      return data;
    })
    .then(initialzePagesText)
    .catch((error) => {
      console.error(error);
    });
}

function tackle(params) {
  if (params.state == 200) {
    let pageMark = {
      current_page: params.pagination[paginationCurrPageKey],
      total_pages: params.pagination[paginationTotalPageKey],
    };

    setToObjectLocalStorage(paginationOrderPageKey, pageMark);
    appendInsertEle(exhibitionTabulationTag, params.pagination.paged_data);
  }
}

function getLocalToken(tokenName) {
  let token = localStorage.getItem(tokenName);
  if (!token) {
    let text = "please try logining in again";
    feedTxtIntoTag(text);
    return false;
  }
  console.log("token: ", token);

  // 添加一个名为'Authorization'的请求头，并将token作为值
  let mineHeader = {
    Authorization: "Bearer " + token,
  };
  return mineHeader;
}

function feedTxtIntoTag(text) {
  if (text) {
    informationTag.textContent = text;
  }
}

function getCookie(name) {
  let nameEQ = name + "=";
  let ca = document.cookie.split(";");

  for (let i = 0; i < ca.length; i++) {
    // 获取当前循环索引位置的 cookie 字符串
    let c = ca[i];

    // 如果当前 cookie 字符串的第一个字符是空格，则删除这个空格并更新 c 的值
    while (c.charAt(0) === " ") {
      c = c.substring(1, c.length); // 将字符串从第一个非空格字符开始截取到结束
    }

    // 检查当前 cookie 名称是否与我们正在寻找的名称相匹配（nameEQ 是目标cookie名称）
    if (c.indexOf(nameEQ) === 0) {
      // 如果在 c 的起始位置找到了 nameEQ
      // 返回该 cookie 的值部分，即从 nameEQ 长度之后到字符串结尾
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
}

function appendInsertEle(targetTagSelector, objectArray) {
  let targetContainer = document.querySelector("." + targetTagSelector);
  targetContainer.innerHTML = ""; // 初始化

  for (let i = 0; i < objectArray.length; i++) {
    let obj = objectArray[i];

    let divElement = document.createElement("div");
    divElement.id = cellDivideNameId + obj["articleid"];
    divElement.classList.add("single-journal-item-div");

    let boxElement = createCheckBoxs(obj["articleid"]);
    let titleElement = createTitleEle("title", obj);
    let timeElement = createTimeEle("time", obj);

    divElement.appendChild(boxElement);
    divElement.appendChild(titleElement);
    divElement.appendChild(timeElement);

    // 将生成的div标签追加到目标容器内
    targetContainer.appendChild(divElement);
  }
}

function createTitleEle(key, obj) {
  if (key == "title") {
    let divide = document.createElement("div");
    let addrEle = document.createElement("a");

    addrEle.textContent = obj[key];
    addrEle.classList.add("title-" + obj["articleid"], "article-link-item");
    // 为按钮元素添加点击事件监听器
    addrEle.onclick = getTagByClassName;

    divide.classList.add(
      "topic-item",
      "journal-single-div",
      "journal-sign",
      "left-journal-design"
    );

    // 将标签添加到div标签内
    divide.appendChild(addrEle);
    return divide;
  }
  return null;
}

function createTimeEle(key, obj) {
  if (key == "time") {
    let divide = document.createElement("div");
    let spanTag = document.createElement("span");

    spanTag.textContent = obj[key];

    divide.classList.add(
      "journal-time-item",
      "journal-single-div",
      "journal-sign",
      "right-journal-design"
    );

    // 将标签添加到div标签内
    divide.appendChild(spanTag);
    return divide;
  }
  return null;
}

function createCheckBoxs(value) {
  let aroundDiv = document.createElement("div");
  // 创建新的input元素
  let checkbox = document.createElement("input");

  // 设置元素属性
  checkbox.type = "checkbox";
  checkbox.value = value;
  checkbox.classList.add("article-box-tag");

  // 如果需要默认勾选，则添加checked属性
  checkbox.checked = false; // 默认状态

  aroundDiv.appendChild(checkbox);
  return aroundDiv;
}

// 设置函数：将对象转化为JSON字符串并存入localStorage
function setToObjectLocalStorage(keyName, value) {
  // 将对象转换为JSON字符串
  let jsonValue = JSON.stringify(value);
  localStorage.setItem(keyName, jsonValue);
}

// 获取函数：从localStorage获取对应的JSON字符串，并转化为对象
function getObjectFromLocalStorageByKey(keyName) {
  // 从localStorage获取JSON字符串
  let jsonString = localStorage.getItem(keyName);
  // 检查是否获取到了值
  if (jsonString !== null) {
    let obj = JSON.parse(jsonString);
    return obj;
  }
  return null; // 或者返回一个默认值，根据你的需求
}

function isEmptyObject(obj) {
  if (obj != null || obj != undefined) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
  }
}
