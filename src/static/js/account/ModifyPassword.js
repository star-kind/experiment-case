let alterPwdHandleToken = "token";
let alterPwdFormTagId = "IdModifyPassWordForm";
let alterPwdInforTagClsName = "information-display";
let cookieStampName = "account_stamp";
let alterPwdKeyDownId = "id-repeat-new-password";
let alterPwdRequestUrl = "/account-modify-password";
let alterPwdUsrTagCls = "passwd-user-name-item";
let cookieExpireDayTime = 1;
let alterPwdNextView = "/";
let delayMinute = 5;

document.addEventListener("DOMContentLoaded", function () {
  initDisplayTag(alterPwdUsrTagCls, cookieStampName);
  enterCommit(alterPwdKeyDownId);
  clicksSubmit(alterPwdFormTagId);
});

function enterCommit(tagId) {
  document.getElementById(tagId).addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      // 或者 event.keyCode === 13
      event.preventDefault(); // 阻止默认行为（例如页面刷新）

      let formData = collectsFormData(alterPwdFormTagId);
      let header = getLocalToken(alterPwdHandleToken);

      if (formData != false && header != false) {
        fetch2Sent(alterPwdRequestUrl, formData, header);
      }
    }
  });
}

function clicksSubmit(tagId) {
  document.getElementById(tagId).addEventListener("submit", function (event) {
    event.preventDefault(); // 阻止默认的表单提交行为

    let formData = collectsFormData(tagId);
    let header = getLocalToken(alterPwdHandleToken);

    if (formData != false && header != false) {
      fetch2Sent(alterPwdRequestUrl, formData, header);
    }
  });
}

function collectsFormData(formId) {
  let formElement = document.getElementById(formId);
  let formData = new FormData(formElement); // 创建FormData对象，包含表单数据

  let newPwd = formData.get("new_password");
  let repeatNewPwd = formData.get("repeat_new_password");

  if (repeatNewPwd != newPwd) {
    let msg = "The new password entered twice is inconsistent";
    setClassText(msg, alterPwdInforTagClsName);
    return false;
  } else if (newPwd.length < 4 || repeatNewPwd.length < 4) {
    let msg = "Password length can not less than 4";
    setClassText(msg, alterPwdInforTagClsName);
    return false;
  } else {
    console.dir(formData);
    return formData;
  }
}

function fetch2Sent(requestUrl, formData, header) {
  fetch(requestUrl, {
    method: "POST",
    body: formData,
    cache: "no-cache", // 对应于false
    headers: header,
  })
    .then((response) => {
      console.log(response);
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Error: " + response.statusText);
      }
    })
    .then(function (response) {
      dispose(response);
    })
    .catch((error) => {
      console.error(error);
    });
}

function dispose(response) {
  console.log(response);
  if (response.state === 200) {
    let text = "Password modification successful, please try logining in again";
    setClassText(text, alterPwdInforTagClsName);

    setTimeout(function () {
      window.location.assign(alterPwdNextView);
    }, 1000 * delayMinute);
  } else {
    setClassText(response.message, alterPwdInforTagClsName);
  }
}

function getLocalToken(tokenName) {
  let token = localStorage.getItem(tokenName);
  if (!token) {
    let text = "please try logining in again";
    setClassText(text, alterPwdInforTagClsName);
    return false;
  }
  console.log("token: ", token);

  // 添加一个名为'Authorization'的请求头，并将token作为值
  let mineHeader = {
    Authorization: "Bearer " + token,
  };
  return mineHeader;
}

function setClassText(text, eleName) {
  if (text) {
    const elements = document.getElementsByClassName(eleName);

    for (let i = 0; i < elements.length; i++) {
      elements[i].textContent = text;
    }
  }
}

function initDisplayTag(eleSelector, cookieName) {
  let eles = document.getElementsByClassName(eleSelector);
  let val = getCookie(cookieName);

  for (let i = 0; i < eles.length; i++) {
    eles[i].textContent = val;
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

function isValidEmail(email) {
  var emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email);
}
