let observationRequestPath = "essay-perusal-ciphertext";
const observeObject = document.querySelector("#observe-button-id");
let observationRequestDealy = 15;
let msgTagClsName = "p.exhibit-exception-post";
const msgTagElements = document.querySelectorAll(msgTagClsName);
let secretElementTag = document.querySelector("#id-secret-input-item");
const mailNameEle = document.getElementsByClassName("special-mailbox-tip");
let currentUsernameCookie = "account_stamp";

let initiallySetHintNone = () => {
  msgTagElements.forEach((element) => {
    element.textContent = "";
  });
};

function bindObservationClickEvent() {
  observeObject.addEventListener("click", function () {
    initiallySetHintNone();

    let keyValue = secretElementTag.value.trim();
    processSubmit(keyValue);
  });
}

let processSubmit = (keyValue) => {
  if (keyValue) {
    console.log(keyValue);

    let offerParam = produceParam(keyValue, initiallyArticleKey);
    let header = getHeaderFromLocal(generateTokenKey);

    if (offerParam && header) {
      instructRequestUrl(observationRequestPath, offerParam, header);
    }
  } else {
    let msg = "You have not yet entered the key for the article";
    setTxtContext(msg);
  }
};

function getHeaderFromLocal(tokenKey) {
  let header = localStorage.getItem(tokenKey);
  if (header == false) {
    let msg = "Account status is abnormal, please sign in again";
    setTxtContext(msg);
    return false;
  }

  // 添加一个名为'Authorization'的请求头，并将token作为值
  let accountToken = {
    Authorization: "Bearer " + header,
  };
  return accountToken;
}

let getArticleId = (articleSign) => {
  let articleID = getValueFromStorage(articleSign).articleid;
  if (articleID == false) {
    let msg =
      "The article data is abnormal. Please try again and click to read";
    setTxtContext(msg);
    return false;
  }
  return articleID;
};

function produceParam(keyValue, articleSign) {
  let articleID = getArticleId(articleSign);
  let offerParam = {
    article_key: keyValue,
    article_id: articleID,
  };

  return offerParam;
}

function setTxtContext(string) {
  if (!string) {
    throw new Error("The parameter cannot be empty");
  }

  for (let i = 0; i < msgTagElements.length; i++) {
    msgTagElements[i].textContent = string;
  }
}

function getValueFromStorage(keyName) {
  // 从local storage中根据keyname取出json string
  const jsonString = localStorage.getItem(keyName);

  // 转为object
  const jsonObject = JSON.parse(jsonString);
  console.log("jsonObject", jsonObject);

  if (!jsonObject) {
    return false;
  }
  return jsonObject;
}

function instructRequestUrl(requestUrl, param, header) {
  fetch(requestUrl, {
    method: "POST",
    body: JSON.stringify(param),
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
    .then((data) => {
      console.log(data);
      successUncover(data);
      return data;
    })
    .then((data) => {
      if (data.state != 200) {
        setTxtContext(data.message, msgTagClsName);
      }
      return data;
    })
    .then((data) => {
      if (data.state == 200) {
        initiallySetHintNone();
      }
    })
    .catch((error) => {
      console.error(error);
    });
}

let successUncover = (data) => {
  if (data.state == 200) {
    contentTextArea.value = "";
    contentTextArea.value = data.article.content;
  }
};

const enterSecretTrigger = () => {
  secretElementTag.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      const inputValue = secretElementTag.value.trim();
      processSubmit(inputValue);
    }
  });
};

let initializeExhibitionMail = () => {
  let mailboxStr = getCookieByName(currentUsernameCookie);
  mailNameEle[0].textContent = mailboxStr;
};

function getCookieByName(name) {
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

enterSecretTrigger();
bindObservationClickEvent();
initializeExhibitionMail();
