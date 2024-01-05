let inforTagClsName = "information-display";
let cookieStampName = "account_stamp";
let cookieExpireDay = 1;
let requestUrl = "/account-register";
let formIdName = "id-register-form";
let keyDownTagId = "id-repeat-password";

document.addEventListener("DOMContentLoaded", function () {
  enterCommit();
  clicksSubmit();
});

function enterCommit() {
  document
    .getElementById(keyDownTagId)
    .addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        // 或者 event.keyCode === 13
        event.preventDefault(); // 阻止默认行为（例如页面刷新）

        let formData = collectsFormData(formIdName);
        if (formData != false) {
          fetch2Sent(requestUrl, formData);
        }
      }
    });
}

function clicksSubmit() {
  document
    .getElementById(formIdName)
    .addEventListener("submit", function (event) {
      event.preventDefault(); // 阻止默认的表单提交行为

      let formData = collectsFormData(formIdName);
      if (formData != false) {
        fetch2Sent(requestUrl, formData);
      }
    });
}

function collectsFormData(formID) {
  let formElement = document.getElementById(formID);
  let formData = new FormData(formElement); // 创建FormData对象，包含表单数据
  let pwd = formData.get("password");
  let re_pwd = formData.get("repeat_password");

  if (pwd !== re_pwd) {
    let text = "The passwords entered twice do not match";
    setClassText(text, inforTagClsName);
    return false;
  } else if (re_pwd.length < 4) {
    let text = "The password length cannot be less than 4 digits";
    setClassText(text, inforTagClsName);
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
      dispose(response, formData.get("email"));
    })
    .catch((error) => {
      console.error(error);
    });
}

function dispose(response, email) {
  console.log(response);
  if (response.state === 200) {
    let text =
      "Registration successful, about to prepare to jump to the login page";
    setClassText(text, inforTagClsName);

    setCookie(cookieStampName, email, cookieExpireDay);

    setTimeout(() => {
      window.location.assign("/");
    }, 2000);
  } else {
    setClassText(response.message, inforTagClsName);
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

function setCookie(name, value, days) {
  var expires = "";
  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}
