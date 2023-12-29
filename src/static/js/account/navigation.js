let usrTagCls = "user-name-item-span";
let cookieStampName = "account_stamp";

window.onload = function () {
  initDisplayTag(usrTagCls, cookieStampName);
};

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
