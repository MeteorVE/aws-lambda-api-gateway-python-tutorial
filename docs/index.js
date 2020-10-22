let url = 'https://7j4rosmvw7.execute-api.us-east-2.amazonaws.com/test/?board=NTU&num=3';

//url = 'https://randomuser.me/api/';

async function fetchBoardInfo() {

  const board = document.getElementById("board").value;
  const num = document.getElementById("num").value;
  url = 'https://7j4rosmvw7.execute-api.us-east-2.amazonaws.com/test/?board=' + board + '&num=' + num
  console.log(url)
  const response = await fetch(url,{
    method: 'GET',
    headers: {
    //       'Access-Control-Allow-Origin': '*',
    //       'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    //       'Access-Control-Allow-Credentials': true,
           'Content-Type': 'application/json'
           
    //        'Access-Control-Request-Method':'GET'

    //       //mode: 'cors'
    }
  }).then(res => res.json())
    .catch(error => console.error('Error:', error))
    .then(response => { console.log('Success:', response); return response});
  // waits until the request completes...

  let res = response;
  result_div = document.getElementById('result');
  removeAllChildNodes(result_div);
  if(res['body']['error'] != 'false'){
    var para = document.createElement("P");
    para.id = pid;
    para.textContent = res['body']['error'];
    result_div.appendChild(para);
  }else{

    const tableDiv = document.getElementById('result');
    const tableNode = document.createElement('table');
    tableNode.id = 'tid'; 
    tableNode.classList.add("table", "table-dark", "w-auto");
    tableDiv.appendChild(tableNode);

    var str = "<tr><td>文章編號</td><td>文章標題</td></tr>";
    for (k in res['body']) {
      if(k == 'error'){
        continue;
      } 
      if (res['body'][k]['title'] == null){
        res['body'][k]['title'] = '[此文已被刪除]';
        res['body'][k]['url'] = '';
      } 
      
      let tmpStr = "<tr><td>" + k +
        "</td><td><a href='" + res['body'][k]['url'] +"'>" + res['body'][k]['title'] + "</a></td></tr>\n";
      str += tmpStr;
    }

    // let table = document.querySelector("#tid");
    //table.classList.remove("displayNone");
    tableNode.innerHTML = str;
 
  }
}

function removeAllChildNodes(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}


//fetchBoardInfo()