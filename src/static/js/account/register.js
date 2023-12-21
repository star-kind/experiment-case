$(document).ready(function () {
  $("#register-form").on("submit", function (event) {
    event.preventDefault(); // 阻止默认的表单提交行为

    var formData = new FormData(this); //创建FormData对象，包含表单数据
    console.dir(formData);

    let pwd = formData.get("password");
    let re_pwd = formData.get("repeat_password");

    if (pwd !== re_pwd) {
      alert("两次输入的密码不匹配");
      return;
    } else if (re_pwd.length < 4) {
      alert("密码长度不能小于4位");
      return;
    }

    $.ajax({
      type: "POST",
      url: "/register-account",
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
    alert("注册成功,点击跳转到登录页面");
    setTimeout(destination, 2000);
  } else {
    alert(response.message);
  }
}

function destination() {
  window.location.assign("/");
}
