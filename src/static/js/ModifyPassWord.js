$(document).ready(function () {
  $("#ModifyPassWord-form").on("submit", function (event) {
    event.preventDefault(); // 阻止默认的表单提交行为

    var formData = new FormData(this);
    console.log(formData);

    var previousPwd = formData.get("previous_password");
    var newPwd = formData.get("new_password");
    var newPwdRepeat = formData.get("repeat_new_password");

    if (previousPwd.length < 4) {
      alert("The previous length can not less than 4.");
      return;
    } else if (newPwd.length < 4) {
      alert("The New Password length can not less than 4.");
      return;
    }
    if (newPwdRepeat.length < 4) {
      alert("The Repeat New Password length can not less than 4.");
      return;
    }

    headers = getHeaders();
    if (headers === false) {
      console.error("Exception");
      return;
    }

    $.ajax({
      type: "POST",
      url: "/handle-modify-password",
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
    alert("密码修改成功");
    setTimeout(destination, 2000);
  } else {
    alert(response.message);
  }
}

function getHeaders() {
  var token = localStorage.getItem("token");

  if ((token === "") | (token === null)) {
    console.log("token is None");
    return false;
  } else {
    console.log("token: " + token);

    // 添加一个名为'Authorization'的请求头，并将token作为值
    var headers = {
      Authorization: "Bearer " + token,
    };

    return headers;
  }
}

function destination() {
  window.location.assign("/");
}
