let loginHandleToken = "token";
let loginFormTagId = "id-login-form";
let loginInforTagClsName = "information-display";
let cookieStampName = "account_stamp";
let loginKeyDownId = "id-password";
let loginRequestUrl = "/account-login";
let nextPageView = "/account-navigation-page";
let loginEmailTagId = "id-email";

document.addEventListener("DOMContentLoaded", function () {
  initInputTag(loginEmailTagId, cookieStampName);
  enterCommit();
  clicksSubmit();
});

function enterCommit() {
  document
    .getElementById(loginKeyDownId)
    .addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        // 或者 event.keyCode === 13
        event.preventDefault(); // 阻止默认行为（例如页面刷新）

        let formData = collectsFormData(loginFormTagId);
        if (formData != false) {
          fetch2Sent(loginRequestUrl, formData);
        }
      }
    });
}

function clicksSubmit() {
  document
    .getElementById(loginFormTagId)
    .addEventListener("submit", function (event) {
      event.preventDefault(); // 阻止默认的表单提交行为

      let formData = collectsFormData(loginFormTagId);
      if (formData != false) {
        fetch2Sent(loginRequestUrl, formData);
      }
    });
}

function collectsFormData(formId) {
  let formElement = document.getElementById(formId);
  let formData = new FormData(formElement); // 创建FormData对象，包含表单数据

  let pwd = formData.get("password");
  if (pwd.length < 4) {
    let text = "The password length must not be less than 4";
    setClassText(text, loginInforTagClsName);
    return false;
  } else {
    console.dir(formData);
    return formData;
  }
}

function fetch2Sent(requestUrl, formData) {
  fetch(requestUrl, {
    method: "POST",
    body: formData,
    cache: "no-cache", // 对应于false
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
    let text = "Login successful, about to jump to the profile page";
    setClassText(text, loginInforTagClsName);

    setTimeout(function () {
      localStorage.setItem(loginHandleToken, response.token);
      window.location.assign(nextPageView);
    }, 1000 * 3);
  } else {
    setClassText(response.message, loginInforTagClsName);
  }
}

function setClassText(text, eleName) {
  if (text) {
    const elements = document.getElementsByClassName(eleName);

    for (let i = 0; i < elements.length; i++) {
      elements[i].textContent = text;
    }
  }
}

function initInputTag(inputID, cookieName) {
  let inputEle = document.getElementById(inputID);
  let val = getCookie(cookieName);

  if (val) {
    inputEle.value = val;
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
