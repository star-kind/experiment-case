let displayStyleVal = "inline-block";
let delaySecondTime = 1.5;
let modifyEncryptRequest = "essay-modify-cipher";
let modifyUncoverRequest = "essay-modify-plain";
let generateTokenKey = "token";
let initiallyArticleKey = "target_article";
let prepareArticleName = "prepare_article";
const editBtn = document.querySelector("#editBtn");
const cancelEditBtn = document.querySelector("#cancelEditBtn");
const saveBtn = document.querySelector("#saveBtn");
const encryptKeyInput = document.querySelector("#id-secret-input-item");
const observeButton = document.querySelector("#observe-button-id");
const titleInput = document.querySelector("#id-alter-title");
const contentTextArea = document.querySelector("#id-alter-content");

window.onload = () => {
  editButtonProcess();
  cancelButtonProcess();
  savelButtonProcess();
  setValueFromStorage(initiallyArticleKey);
};

function setValueFromStorage(keyName) {
  // 从local storage中根据keyname取出json string
  const jsonString = localStorage.getItem(keyName);

  // 转为object
  const jsonObject = JSON.parse(jsonString);
  console.log(jsonObject);

  // 赋予input标签的value
  titleInput.value = jsonObject.title;
  contentTextArea.value = jsonObject.content;
}

let editButtonProcess = () => {
  editBtn.addEventListener("click", () => {
    initiallySetHintNone();

    titleInput.readOnly = false;
    contentTextArea.readOnly = false;

    editBtn.style.display = "none";
    observeButton.style.display = "none";

    cancelEditBtn.style.display = displayStyleVal;
    saveBtn.style.display = displayStyleVal;

    const data = {
      title: titleInput.value,
      content: contentTextArea.value,
    };
    localStorage.setItem(prepareArticleName, JSON.stringify(data));
  });
};

let cancelButtonProcess = () => {
  cancelEditBtn.addEventListener("click", () => {
    initiallySetHintNone();
    ready4CancleStatus();

    const storedData = localStorage.getItem(prepareArticleName);
    if (storedData) {
      const data = JSON.parse(storedData);
      titleInput.value = data.title;
      contentTextArea.value = data.content;
    }
  });
};

let ready4CancleStatus = () => {
  titleInput.readOnly = true;
  contentTextArea.readOnly = true;

  editBtn.style.display = displayStyleVal;
  observeButton.style.display = displayStyleVal;

  cancelEditBtn.style.display = "none";
  saveBtn.style.display = "none";
};

let savelButtonProcess = () => {
  saveBtn.addEventListener("click", () => {
    initiallySetHintNone();
    setTimeout(ready4Save, delaySecondTime * 1000);
  });
};

let ready4Save = () => {
  titleInput.readOnly = true;
  contentTextArea.readOnly = true;

  editBtn.style.display = displayStyleVal;
  observeButton.style.display = displayStyleVal;

  cancelEditBtn.style.display = "none";
  saveBtn.style.display = "none";

  const data = {
    title: titleInput.value,
    content: contentTextArea.value,
  };
  localStorage.setItem(prepareArticleName, JSON.stringify(data));

  submitMethod();
};

let getPrepareParameters = () => {
  let articleID = getArticleId(initiallyArticleKey);
  let tokenHead = getHeaderFromLocal(generateTokenKey);

  let assemblyParam = {
    new_title: titleInput.value.trim(),
    new_content: contentTextArea.value.trim(),
    secret_key: encryptKeyInput.value.trim(),
    header: tokenHead,
    article_id: articleID,
  };

  console.log("getPrepareParameters", assemblyParam);
  return assemblyParam;
};

let triggerCtrlEnterEvent = (event) => {
  if (
    event.ctrlKey &&
    event.key === "Enter" &&
    contentTextArea.readOnly == false
  ) {
    submitMethod();
  }
};

let modifyTextAreaTrigger = () => {
  contentTextArea.addEventListener("keydown", (event) => {
    triggerCtrlEnterEvent(event);
  });
};

let submitMethod = () => {
  let parameters = getPrepareParameters();
  let tmpObj = reduceBuildObj(parameters, "header");

  if (parameters.secret_key) {
    console.log(modifyEncryptRequest);
    emitToRequest(modifyEncryptRequest, tmpObj, parameters.header);
  } else {
    console.log(modifyUncoverRequest);
    emitToRequest(modifyUncoverRequest, tmpObj, parameters.header);
  }
};

function emitToRequest(requestUrl, param, header) {
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
      victoriesReq(data);
      return data;
    })
    .then((data) => {
      setTimeout(victoriesReq2(data, param), 3 * 1000);
      return data;
    })
    .then((data) => {
      setTimeout(victoriesReq3(data, param), 3 * 1000);
      return data;
    })
    .then((data) => {
      if (data.state != 200) {
        setTxtContext(data.message);
      }
      return data;
    })
    .then((data) => {
      if (data.state == 200) {
        ready4CancleStatus();
      }
      return data;
    })
    .catch((error) => {
      console.error(error);
    });
}

let victoriesReq = (data) => {
  if (data.state == 200) {
    setTxtContext("Article change successful");
    setTimeout(initiallySetHintNone, 1000 * 10);
  }
};

let victoriesReq2 = (data, tempParam) => {
  if (data.state == 200 && data.grade == 0) {
    titleInput.value = tempParam.new_title;
    contentTextArea.value = tempParam.new_content;

    let localObj = JSON.parse(localStorage.getItem(initiallyArticleKey));
    console.log("localObj", localObj);

    localObj.title = tempParam.new_title;
    localObj.content = tempParam.new_content;
    localStorage.setItem(initiallyArticleKey, JSON.stringify(localObj));
  }
};

let victoriesReq3 = (data, tempParam) => {
  if (data.state == 200 && data.grade == 1) {
    titleInput.value = tempParam.new_title;
    contentTextArea.value = data.content;

    let localObj = JSON.parse(localStorage.getItem(initiallyArticleKey));
    console.log("localObj", localObj);

    localObj.title = tempParam.new_title;
    localObj.content = data.content;
    localStorage.setItem(initiallyArticleKey, JSON.stringify(localObj));

    secretElementTag.value = "";
  }
};

let reduceBuildObj = (paramObject, excludeKey) => {
  let tmp = {};
  for (let key in paramObject) {
    if (key != excludeKey) {
      tmp[key] = paramObject[key];
    }
  }
  console.log("reduceBuildObj", tmp);
  return tmp;
};

modifyTextAreaTrigger();
