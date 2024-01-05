let composeEmitReqUrl = "essay-growth-single";
let cilentTokenKey = "token";
let userCookieName = "account_stamp";
let paramterItemCls = "paramter-side";
let targetNoteTemporaryKey = "target_article";
let viewArticlePagePath = "essay-blog-perusal-page";
let postAccountElement = document.querySelector("#post-name-side");
let postBackMsgElement = document.querySelector("#post-alert-space");
let buttonEleObj = document.querySelector("#deliver-press");
let clearResetBtnObj = document.querySelector("#clean-all-press");
let texrAreaObj = document.querySelector("#id-ele-content");
let inputTitleEleId = document.querySelector("#id-input-title");
let inputTexeAreaTagId = document.querySelector("#id-ele-content");
let delaySecondNumber = 3;

let initializationLoad = () => {
  postEmailInTag();
  buttonsBindClickEvent();
};

let postEmailInTag = () => {
  let cookieValue = getCookieValue(userCookieName);
  if (cookieValue) {
    postAccountElement.textContent = cookieValue;
  }
};

function getCookieValue(name) {
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

let indicateMsgAtTag = (str) => {
  if (str) {
    postBackMsgElement.textContent = str;
  }
};

function buttonsBindClickEvent() {
  buttonEleObj.addEventListener("click", deliverParam2Req);
  clearResetBtnObj.addEventListener("click", resetInputsParamters);
  elementBindCtrlEnter();
}

function elementBindCtrlEnter() {
  texrAreaObj.addEventListener("keydown", (event) => {
    if (event.ctrlKey && event.key === "Enter") {
      deliverParam2Req();
    }
  });
}

let gainParamtersFromTag = () => {
  let elements = document.getElementsByClassName(paramterItemCls);
  let result = {};
  for (let i = 0; i < elements.length; i++) {
    result[elements[i].name] = elements[i].value.trim();
  }
  console.log("gainParamtersFromTag", result);

  if (!result.title || !result.content) {
    indicateMsgAtTag("The title or content not inputted yet");
    setTimeout(() => {
      postBackMsgElement.textContent = "";
    }, 1000 * 20);
    return false;
  }

  return result;
};

let resetInputsParamters = () => {
  let elements = document.getElementsByClassName(paramterItemCls);
  for (let i = 0; i < elements.length; i++) {
    elements[i].value = "";
  }
};

function getStorageToken() {
  let header = localStorage.getItem(cilentTokenKey);
  if (header == false) {
    let msg = "Account status is abnormal, please sign in again";
    indicateMsgAtTag(msg);
    return false;
  }

  // 添加一个名为'Authorization'的请求头，并将token作为值
  let accountToken = {
    Authorization: "Bearer " + header,
  };

  console.log("getStorageToken", accountToken);
  return accountToken;
}

let deliverParam2Req = () => {
  let paramter = gainParamtersFromTag();
  let userHeader = getStorageToken();

  if (!paramter || !userHeader) {
    return;
  }

  fetch(composeEmitReqUrl, {
    method: "POST",
    body: JSON.stringify(paramter),
    cache: "no-cache", // 对应于false
    headers: userHeader,
    contentType: "application/json",
  })
    .then((response) => {
      console.log(response);
      if (response.ok) {
        return response.json();
      } else {
        throw new Error(response.statusText);
      }
    })
    .then((data) => {
      console.log(data);
      successfullyProcess(data);
      return data;
    })
    .then((data) => {
      subjectExist(data);
      return data;
    })
    .then((data) => {
      if (data.state == 200) {
        setTimeout(() => {
          window.location.assign(viewArticlePagePath);
        }, 1000 * delaySecondNumber);
      }
      return data;
    })
    .then((data) => {
      if (data.state == 200) {
        indicateMsgAtTag("Successfully codify the article");
      }
      return data;
    })
    .then((data) => {
      if (data.state != 200) {
        indicateMsgAtTag(data.message);
      }
      return data;
    })
    .catch((error) => {
      console.error(error);
    });
};

let successfullyProcess = (result) => {
  if (result.state == 200) {
    indicateMsgAtTag("The article was successfully written");
  }
};

let subjectExist = (result) => {
  if (result.state == 200 && result.review) {
    let objStr = JSON.stringify(result.review);
    localStorage.setItem(targetNoteTemporaryKey, objStr);
  }
};

initializationLoad();
