$(document).ready(function () {
  $("#login-form").on("submit", function (event) {
    event.preventDefault(); // 阻止默认的表单提交行为
    var formData = new FormData(this); //创建FormData对象，包含表单数据

    let pwd = formData.get("password");
    if (pwd.length < 4) {
      alert("密码长度不能小于4位");
      return;
    }

    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8085/login",
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
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
    sendRequest(response.token);
    alert("登录成功,点击跳转到资料页面");
    setTimeout(assignPage, 2000);
  } else {
    alert(response.message);
  }
}

function assignPage() {
  window.location.assign("http://127.0.0.1:8085/modify-email");
}

function sendRequest(token) {
  localStorage.setItem("token", token);
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
    type: "GET",
    headers: headers,
    url: "http://127.0.0.1:8085/modify-email",
    success: function (response) {
      console.log(response);
    },
    error: function (error) {
      console.error(error);
    },
  });
}
