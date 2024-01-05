let viewElementClsName = "article-link-item";
let perusalTextRequestUrl = "essay-perusal-plain";
let successAfterPage = "essay-blog-perusal-page";
let targetArticleKey = "target_article";
let clickViewDelaySecond = 1;

function getTagByClassName() {
  const classNames = this.className.split(" ");
  let articleID = getNumberFromString(classNames[0]);

  assembleParam(paginationTokenKey, articleID);
}

function assembleParam(tokenKey, articleID) {
  let header = getLocalToken(tokenKey);
  if (header == false) {
    let msg = "Account status is abnormal, please sign in again";
    feedTxtIntoTag(msg);
    return;
  }

  let offerParam = { article_id: articleID };

  embedRequestUrl(perusalTextRequestUrl, offerParam, header);
}

function embedRequestUrl(requestUrl, param, header) {
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
      arrange(data);
      return data;
    })
    .then((data) => {
      return crashProcess(data);
    })
    .then((data) => {
      onwards(data);
    })
    .catch((error) => {
      console.error(error);
    });
}

function arrange(result) {
  if (result.state == 200) {
    setToObjectLocalStorage(targetArticleKey, result.article);
  }
}

function getNumberFromString(str) {
  const parts = str.split("-");
  let articleID = parseInt(parts[1], 10);

  console.log("articleID", articleID);
  return articleID;
}

let onwards = (data) => {
  if (data.state == 200) {
    setTimeout(() => {
      window.location.assign(successAfterPage);
    }, clickViewDelaySecond * 1000);
  }
};

let crashProcess = (data) => {
  if (data.state != 200) {
    feedTxtIntoTag(data.message);
  }
  return data;
};
