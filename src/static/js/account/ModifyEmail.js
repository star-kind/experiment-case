// 比传统的window.onload更快
document.addEventListener("DOMContentLoaded", sendRequest);

function sendRequest() {
  var token = localStorage.getItem("token");
  if ((token === "") | (token === null)) {
    console.log("token is None");
    return;
  }
  console.log("token: " + token);
}

$(document).ready(function () {
  $("#ModifyEmail-form").on("submit", function (event) {
    event.preventDefault(); // 阻止默认的表单提交行为

    var formData = new FormData(this);
    console.log(formData);

    var password = formData.get("password");
    var newEmail = formData.get("new_email");

    if (!isValidEmail(newEmail)) {
      alert("The New email address is invalid.");
      return;
    } else if (
      (password === "") |
      (password === null) |
      (password === undefined)
    ) {
      alert("please input Password.");
      return;
    } else if (password.length < 4) {
      alert("Password length can not less than 4.");
      return;
    }

    var token = localStorage.getItem("token");
    if ((token === "") | (token === null)) {
      console.log("token is None");
      return;
    }
    console.log("token: " + token);

    // 添加一个名为'Authorization'的请求头，并将token作为值
    var headers = {
      Authorization: "Bearer " + token,
    };

    $.ajax({
      type: "POST",
      url: "/handle-modify-email",
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
      headers: headers,
      success: dispose,
      error: function (jqXHR, textStatus, errorThrown) {
        console.error(textStatus, errorThrown);
      },
    });
  });
});

function dispose(response) {
  console.log(response);
  if (response.state === 200) {
    localStorage.setItem("token", response.token);
    alert("邮箱地址更换成功");
    setTimeout(destination, 2000);
  } else {
    alert(response.message);
  }
}

function isValidEmail(email) {
  var emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email);
}

function destination() {
  window.location.assign("/");
}
