let deleteRequestUrl = "essay-delete-multiple";
let triggerBoxElement = document.querySelector("#id-control-box-trigger");
let deleteEssayBtnEle = document.querySelector("#id-delete-button-execute");
let checkBoxClassName = ".article-box-tag";
let timeNumberValue = 5;

let initializeDeleteInstance = () => {
  bindDeleteCilckEvent();
  bindControlTriggerEvent();
};

let bindDeleteCilckEvent = () => {
  // 为按钮元素绑定点击事件
  deleteEssayBtnEle.addEventListener("click", pushCommit);
};

let pushCommit = () => {
  let param = gainCheckedArray();

  if (param == false) {
    let hint = "No article has been selected yet";
    feedTxtIntoTag(hint);

    setTimeout(() => {
      informationTag.textContent = "";
    }, 15 * 1000);
  } else {
    let reqHeader = getLocalToken(paginationTokenKey);
    let data = { article_list: param };

    pushParameter2Request(deleteRequestUrl, data, reqHeader);
  }
};

let bindControlTriggerEvent = () => {
  triggerBoxElement.addEventListener("click", () => {
    let checkboxes = document.querySelectorAll(
      "input[type='checkbox']" + checkBoxClassName
    );
    for (let i = 0; i < checkboxes.length; i++) {
      checkboxes[i].checked = triggerBoxElement.checked;
    }
  });
};

let gainCheckedArray = () => {
  // 获取所有类名为 "cls-ok" 且已被勾选的类型为 checkbox 的 input 标签元素对象
  let checkedCheckboxes = document.querySelectorAll(
    "input[type='checkbox']" + checkBoxClassName + ":checked"
  );
  let valuesArray = [];

  for (let i = 0; i < checkedCheckboxes.length; i++) {
    valuesArray.push(Number(checkedCheckboxes[i].value));
  }
  console.log("gainCheckedArray", valuesArray); // 输出包含所有元素的 value 的数组

  if (valuesArray.length == 0) {
    return false;
  }
  return valuesArray;
};

let pushParameter2Request = (requestUrl, param, header) => {
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
      victoryReport(data, param);
      return data;
    })
    .then((data) => {
      setTimeout(victoryAfterDisplay(data, param), 1000 * timeNumberValue);
      return data;
    })
    .then((data) => {
      if (data.state != 200) {
        feedTxtIntoTag(data.message);
      }
      return data;
    })
    .catch((error) => {
      console.error(error);
    });
};

let victoryReport = (data, param) => {
  if (data.state == 200) {
    let hint =
      "Successfully deleted " + param.article_list.length + " articles";
    feedTxtIntoTag(hint);
  }
};

let victoryAfterDisplay = (data, param) => {
  if (data.state == 200) {
    for (let index = 0; index < param.article_list.length; index++) {
      let idValue = param.article_list[index];
      let name = cellDivideNameId + idValue;
      let selector = document.querySelector("#" + name);
      selector.style.display = "none";
    }
  }
};

initializeDeleteInstance();
