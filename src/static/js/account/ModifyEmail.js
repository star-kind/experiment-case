let modifyMailHandleToken = "token";
let modifyMailFormTagId = "ID-ModifyEmailForm";
let modifyMailInforTagClsName = "information-display";
let cookieStampName = "account_stamp";
let modifyMailKeyDownId = "id-password";
let modifyMailRequestUrl = "/account-modify-email";
let modifyMailEmailTagId = "id-email";
let modifyMailUsrTagCls = "user-mail-item";
let cookieExpireDayTime = 1;
let disposeDelayTime = 3;

document.addEventListener("DOMContentLoaded", function () {
  initialEmailTag();
  initDisplayTag(modifyMailUsrTagCls, cookieStampName);
  enterCommit();
  clicksSubmit();
});

function initialEmailTag() {
  let ele = document.getElementById("id-new-email");
  ele.value = "";
}

function enterCommit() {
  document
    .getElementById(modifyMailKeyDownId)
    .addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        // 或者 event.keyCode === 13
        event.preventDefault(); // 阻止默认行为（例如页面刷新）

        let formData = collectsFormData(modifyMailFormTagId);
        let header = getLocalToken(modifyMailHandleToken);

        if (formData != false && header != false) {
          fetch2Sent(modifyMailRequestUrl, formData, header);
        }
      }
    });
}

function clicksSubmit() {
  document
    .getElementById(modifyMailFormTagId)
    .addEventListener("submit", function (event) {
      event.preventDefault(); // 阻止默认的表单提交行为

      let formData = collectsFormData(modifyMailFormTagId);
      let header = getLocalToken(modifyMailHandleToken);

      if (formData != false && header != false) {
        fetch2Sent(modifyMailRequestUrl, formData, header);
      }
    });
}

function collectsFormData(formId) {
  let formElement = document.getElementById(formId);
  let formData = new FormData(formElement); // 创建FormData对象，包含表单数据

  let pwd = formData.get("password");
  if (pwd.length < 4) {
    let text = "The password length must not be less than 4";
    setClassText(text, modifyMailInforTagClsName);
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
      dispose(response, formData.get("new_email"));
    })
    .catch((error) => {
      console.error(error);
    });
}

function dispose(response, email) {
  console.log(response);
  if (response.state === 200) {
    let text = "Email address successfully changed";
    setClassText(text, modifyMailInforTagClsName);

    setCookie(cookieStampName, email, cookieExpireDayTime);

    setTimeout(function () {
      localStorage.setItem(modifyMailHandleToken, response.token);
      location.reload();
    }, 1000 * disposeDelayTime);
  } else {
    setClassText(response.message, modifyMailInforTagClsName);
  }
}

function getLocalToken(tokenName) {
  let token = localStorage.getItem(tokenName);
  if (!token) {
    let text = "please try logining in again";
    setClassText(text, modifyMailInforTagClsName);
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

function setCookie(name, value, days) {
  var expires = "";
  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
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

// // 比传统的window.onload更快
// document.addEventListener("DOMContentLoaded", sendRequest);

// function sendRequest() {
//   var token = localStorage.getItem("token");
//   if ((token === "") | (token === null)) {
//     console.log("token is None");
//     return;
//   }
//   console.log("token: " + token);
// }

// $(document).ready(function () {
//   $("#ModifyEmail-form").on("submit", function (event) {
//     event.preventDefault(); // 阻止默认的表单提交行为

//     var formData = new FormData(this);
//     console.log(formData);

//     var password = formData.get("password");
//     var newEmail = formData.get("new_email");

//     if (!isValidEmail(newEmail)) {
//       alert("The New email address is invalid.");
//       return;
//     } else if (
//       (password === "") |
//       (password === null) |
//       (password === undefined)
//     ) {
//       alert("please input Password.");
//       return;
//     } else if (password.length < 4) {
//       alert("Password length can not less than 4.");
//       return;
//     }

//     var token = localStorage.getItem("token");
//     if ((token === "") | (token === null)) {
//       console.log("token is None");
//       return;
//     }
//     console.log("token: " + token);

//     // 添加一个名为'Authorization'的请求头，并将token作为值
//     var headers = {
//       Authorization: "Bearer " + token,
//     };

//     $.ajax({
//       type: "POST",
//       url: "/handle-modify-email",
//       data: formData,
//       cache: false,
//       contentType: false,
//       processData: false,
//       headers: headers,
//       success: dispose,
//       error: function (jqXHR, textStatus, errorThrown) {
//         console.error(textStatus, errorThrown);
//       },
//     });
//   });
// });

// function dispose(response) {
//   console.log(response);
//   if (response.state === 200) {
//     localStorage.setItem("token", response.token);
//     alert("邮箱地址更换成功");
//     setTimeout(destination, 2000);
//   } else {
//     alert(response.message);
//   }
// }

// function isValidEmail(email) {
//   var emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
//   return emailRegex.test(email);
// }

// function destination() {
//   window.location.assign("/");
// }
