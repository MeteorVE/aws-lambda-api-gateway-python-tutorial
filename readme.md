註 : 此原為預計放在部落格之文章，故記錄方式以主題式陳述。

[DEMO請點我](https://meteorve.github.io/aws-lambda-api-gateway-python-tutorial/)
[備站](http://176.34.9.136:8888/)

<!-- more -->



# 究極的懶人包

這篇算是記錄一點冤枉路，但官方在某篇 tutorial 其實介紹的很不錯
(我做完全部才看到該教學)

雖然自己解還是比較扎實一點，但如果想在短時間搭建出該服務
可以直接造訪，跟著做。

[建立基本 Web 應用程式](https://aws.amazon.com/tw/getting-started/hands-on/build-web-app-s3-lambda-api-gateway-dynamodb/?e=gs2020&p=fullstack)


如果想要了解自己做會遇到什麼問題，或是客製化更多細項
也歡迎查閱下方其他 title 介紹的項目。


# 認識 Lambda


首先我們要知道 ... 你可以想像你正要利用 Lambda 實作 RESTful API。
外部(可能是前端)通過某個方式，傳送一個 json 檔案給 Lambda
然後 Lambda 經過某些處理，也回傳一個 json 檔案回去。

Lambda 做的就是幫忙中介處理的角色
你不需要額外建一個 Server，你不需要開 port 或是處理接口相關
這邊就是一個處理點，若你想連 DB，你可以透過 Lambda 再另外做連接
(但畢竟是 AWS 相關產品，可以連的 ... 就會是 AWS 相關其他服務 ex:EC2 ...)

了解了 Lambda 所在的角色之後，我很建議先看過這篇。
https://aws.amazon.com/tw/getting-started/hands-on/run-serverless-code/

跟著做一次(不過 python 選 3.7 沒關係)，然後我們可以瞭解到他大概的運作


這邊多解釋一些東西 : 

- 設定測試事件 : 我們可以把這個當成是前端，寫一個 json 傳出去
    例如 : ``{'location':'Taipei'}`` (這邊先不用改)
- 預設的 python code，功用只是讀了你傳的 json (包在 event 裡面)，然後回傳第一個給你
    以下是預設的範例 code。
```python
def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print("value1 = " + event['key1'])
    print("value2 = " + event['key2'])
    print("value3 ? = " + event['key3'])
    return event['key1']  # Echo back the first key value
    #raise Exception('Something went wrong')

```


為了更好的了解誰傳入、誰處理、怎麼讀傳入的東西 ... 等等，這邊另外做一個例子解釋。

首先，新增一個測試事件

![](https://i.imgur.com/fG1C0R8.png)

事件範本並不重要，我們簡單就好。

![](https://i.imgur.com/HBMUrOW.png)

建立好之後，我把 lambda_function.py 裡面的內容改成 : 

```python lambda_function.py
import json

def lambda_handler(event, context):
    print("您查詢的城市:" + event['location'])
    # Do some backend process, 
    # we get the information: Taipei is raining.
    return {"Taipei":"Raining"}
```

按下測試按鈕，沒意外的話你會得到以下 : 

```
Response:
{
  "Taipei": "Raining"
}
```

我想，做到這邊你應該更瞭解 Lambda 的用途是什麼，以及該怎麼使用他了。


# 如何引入自己的函式庫


然而，Lambda 那個環境並不能使用第三方的 python libaray
你必須自己上傳該函式庫上去。

這邊提供一個我比較喜歡的方式 : 建 virtualenv，再拿該 Lib 上傳。

之前聽聞可以上傳 virtualenv 上去什麼的，不是很懂，自己亂試+關鍵字才查到這篇文
[“errorMessage”: “Unable to import module 'lambda_function'”](https://stackoverflow.com/questions/48984720/errormessage-unable-to-import-module-lambda-function)

這邊簡介一下 : 
1. 先找一個你習慣工作的目錄，也許他叫 ``project``。``cd project``
    或是你在 ``project`` 啟動你的 terminal。
2. ``virtualenv venv --python=python3.6``，這邊的 python 3.6 可以換成你 local 的版本。
    - 如果你是 Windows，請參考你環境變數內的 python 程式命名。
    - 例如我這邊是 ``virtualenv venv --python=python3.exe
``
3. 如果你在 Linux，請使用 ``source venv/bin/activate`` 來做虛擬環境啟動。
    如果是在 Windows，請使用 ``source venv/Scripts/activate``
4. ``pip install some_lib``，例如我想要裝 numpy，就 ``pip install numpy``
  - 通常 pip 都需要先 upgrade 才能使用，如果出現相關訊息，可以先按照他寫的方式升級。 
5. 如果你在 windows，你會發現創建了一個 venv 的資料夾，進到
    ``venv/lib/python3.6/site-packages`` 裡面，你會看到很多資料夾
    這些都是不同套件，請找你需要的，把他複製出去，假設放在 ``project`` 資料夾吧。
    (Linux 請使用 cp 去複製
    例如 ``cp -r venv/lib/python3.6/site-packages/* .``)
6. 選取那些套件資料夾，以及你的 python 檔案。壓縮起來，上傳上去即可。
  - python 檔案讓他命名 ``lambda_function.py``，也就是跟範例檔案一樣，這樣就能抓到


以下是檔案結構舉例

```txt 檔案結構舉例
project.zip
└ numpy/底下很多套件本身的東西
└ cv2/底下很多套件本身的東西
└ request/底下很多套件本身的東西
└ lambda_function.py
```


其實，也不一定要命名成 ``lambda_function.py``
不過因為當初我們新建 Lambda 函數時，是走自動 example 幫我們建好的
所以如這張圖片顯示，處理常式是 ``lambda_function.lambda_handler``
( lambda_function 檔案裡面的 lambda_handler() 函式。)
所以也能改成自己的，像是 main.py 搭配 lambda_handler()  這樣。

![](https://i.imgur.com/UXgr0Zq.png)

順帶一提，如果你的程式需要跑比較久，記得把 timeout 時間設定久一點 (有個 "逾時" 的欄位)
像是我的從 3 秒改成 10 秒，彈性比較大。



# API Gateway

有了這個 api gateway，我們才能將我們的 Lambda 和前端做一個資訊交換。

## 建立

1. AWS -> Service 選擇 API Gateway -> 建立 API -> 找到 RESTful API 選建置
  然後將資訊填一下，設定名字就好 
  ![](https://i.imgur.com/NRv3c3E.png)

2. 建立方法，我這邊是建 GET，然後把名字等等填一下
  有遇到問連接 Lambda 的函數的話，那邊填你在 Lambda 的 project 名字。
  他會問你是否確定要連接。
  ![](https://i.imgur.com/I9SdzKT.png)

3. 進到 **整合請求**，點最下面映射範本，設定如圖。
  要自己按新增映射範本，輸入 ``application/json``
  下方的映射範本，則是看你的 Field 有哪些，
  例如我傳入的參數就兩個 : board、num，可以按照自己的改相對應字串。
  記得按下面的儲存。
    - **注意 : 冒號後面的全部都要用雙引號刮起來。**
  ![](https://i.imgur.com/0ooZjTS.png)

```
    #set($inputRoot = $input.path('$'))
    {
        "board": "$input.params('board')",
        "num": "$input.params('num')"
    }
```
4. Deploy，也就是部署 API，點了之後會問你階段名稱，你可以打 dev、或是 test 之類的。
  成功部署之後，他會給你一個網址，你就可以用那個網址做測試了。
  ![](https://i.imgur.com/WwtIYSA.png)
5. 測試方式 : 瀏覽器直接輸入該網址，並且加上參數。
  舉例 : ``https://7jpojemvw7.execute-api.us-east-2.amazonaws.com/test/?board=Taipei&num=3``
  可以將其拆解為 ``他提供給你複製的網址/?key1=value1&key2=value2``
  以上請自行替換，我的兩個 key 分別是 board 和 num，我想應該舉例的算清楚。
  

## 開啟 CORS

1. 從 "操作" 去點選 **啟用 CORS**
  ![](https://i.imgur.com/fMc1jlx.png)
2. 然後其實預設的就差不多了，儲存
  ![](https://i.imgur.com/6ujK4pP.png)
3. 部署 API，忘記的可以參考上面的第四步驟。


- 一些官方教學
  - [官方文件: how-to-cors](https://docs.aws.amazon.com/zh_tw/apigateway/latest/developerguide/how-to-cors.html)
  - [官方文件: 測試 CORS](https://docs.aws.amazon.com/zh_tw/apigateway/latest/developerguide/apigateway-test-cors.html)
    - 在做這個的時候，記得指令是 ``curl -v -X OPTIONS https://your_api_url_and_parameter`` 
      - -v 代表列出溝通過程，-X OPTIONS 是會再從中選某些設定。
      - OPTIONS 記得要打 ! 
      - 然後就能看到 ``Access-Control-Allow-Origin: *`` 和 ``Access-Control-Allow-Headers``



## 此階段可能遇到的問題 : 

### 參數傳不進去，明明 Lambda 那邊跑測試沒問題。

如果拿去測試，卻發現參數傳不進去 (這點你可以從回傳的資訊發現，他會告訴你卡在後端哪行。)
因為後端你從 event 去提取參數，若你沒成功傳入，他則會讀到 None
後面如果有用到計算，可能就會直接造成 Lambda 端崩潰。

這部分請檢查上面第三點的 **整合請求** 有沒有遇到問題
我的**映射範本**是改了很多次，查了很多地方最後才確認是那樣寫的
那邊寫錯就會直接卡住。

另外提一下，其實後來看了一下官方在整合請求這部分的說明   
其實如果我們不去新增映射範本，
即使遇到 Content-Type 未指定的情況 (送 request 的 header 沒有含 Content-Type)
他也會自己把它判為 application/json。

![](https://i.imgur.com/9WjwQTP.png)

- [官方對整合傳遞行為的解釋](https://docs.aws.amazon.com/zh_tw/apigateway/latest/developerguide/integration-passthrough-behaviors.html)


### CORS 問題還是無法解決

這邊我卡了很久。
主要是前端 fetch 那邊，我不知道 header 該放哪些參數
又看了有些討論以及官方文檔說要在 Lambda 的 return 裡面加上 header
感覺都做了卻還是一直出現 CORS 問題。

最後，我發現反而是我給太多 Header 了，然後伺服器拒收。
(感謝大神朋友幫忙找問題 ...)

這邊放一下最終我前端寫的資訊 

```JS index.js
const response = await fetch(url,{
    method: 'GET',
    headers: {
           'Content-Type': 'application/json'
    }
  }).then(res => res.json()) // 要轉成 json 才能在 console 看懂
    .catch(error => console.error('Error:', error))
    .then(response => { console.log('Success:', response); return response});
    // 如果沒有寫 return response，你的 const response 仍然是 null。
```

相見恨晚，我解決的隔天同學貼了個這個給我看 
([官方文檔: 新增互動性至您的 Web 應用程式](https://aws.amazon.com/tw/getting-started/hands-on/build-web-app-s3-lambda-api-gateway-dynamodb/module-five/))
雖然因為他的範例和我自己做得有些許不一樣，但主要參考 header 部分就好。

```JS
var callAPI = (firstName,lastName)=>{
            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            var raw = JSON.stringify({"firstName":firstName,"lastName":lastName});
            var requestOptions = {
                method: 'POST',
                headers: myHeaders,
                body: raw,
                redirect: 'follow'
            };
            fetch("YOUR-API-INVOKE-URL", requestOptions)
            .then(response => response.text())
            .then(result => alert(JSON.parse(result).body))
            .catch(error => console.log('error', error));
        }
```



以及後端在做 return 會回傳的東西。
(參考 : [官方文件: how-to-cors](https://docs.aws.amazon.com/zh_tw/apigateway/latest/developerguide/how-to-cors.html) )

```python 
def lambda_handler(event, context):
  # some code
  # ...
  
  return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': "*",
            "Access-Control-Allow-Credentials" : "true",
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': my_json_file # 換成你要 return 的資訊，type: dictionary
    };
```

跑測試的時候，得到的 response 大概會長這樣 : 
![](https://i.imgur.com/XRPs3C4.png)



# 串前端



其實在前面，把 Lambda、API Gateway、CORS 部分都處理好之後，
串前端的部分就是看你要做得好還是做的爛了 (x)

可以不套 CSS 就完成練習，也能默默地美化好 (?)

個人因為搭配前一個作業，利用 Docker 去跑一個 apache，所以就把我的前端檔案佈署過去，就沒什麼問題了。
而且因為 CORS 處理好了，所以其實用 Local file 也能做 fetch 的動作，
Local 運作沒問題，上傳上去也不會有太大問題。

如果懶得也不想自己弄一個 Server 環境，可以參考 AWS 的 Amplify 平台
你只要把 index.html 等等壓縮成 zip 然後上傳就可以跑了，超無腦。 



# 成果展示



Lambda 那邊做了爬蟲，爬蟲結果回傳前端，差不多是這次做的東西。
其實處理時間大概要 4~5 秒 (因為不是純爬 html)，只是用 GIF 呈現所以把那些 frame 剪掉了 XD



![](https://i.imgur.com/kw3zZha.gif)





# Note

For 迴圈在 JS 該 in 還是 of : 

- [Src](https://kanboo.github.io/2018/01/30/JS-for-of-forin/)

1. 建議：在迭代物件屬性時，使用 `for...in`；在迭代陣列時，使用 `for...of`。
2. `for...in` 輸出的是屬性名稱(key)，`for...of` 輸出的是值(value)
3. `for...of` 是 ES6 的新語法。修復了ES5 for…in 的不足
4. `for...of` 不能迭代物件，需要透過和 Object.keys() 搭配使用



- table 如果想要一格有三格寬可以使用 ``<td colspan='3'>``
- table 如果想要平均分配列寬可以使用 ``table-layout: fixed;``
- 如果套了 bootstrap 4 有一些強制 width 100%，可以在 class 加 `` w-auto ``
  - [ref](https://stackoverflow.com/questions/10687306/why-do-twitter-bootstrap-tables-always-have-100-width)



# Other Ref

[Using_Fetch](https://developer.mozilla.org/zh-TW/docs/Web/API/Fetch_API/Using_Fetch)

[CORS 介紹 by mozilla](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/CORS)

[一些 form 傳遞範例](https://gist.github.com/justsml/529d0b1ddc5249095ff4b890aad5e801)

[onclick 複習](https://www.w3schools.com/jsref/event_onclick.asp)

[愷開也有紀錄關於 CORS](https://medium.com/d-d-mag/%E5%92%8C-cors-%E8%B7%9F-cookie-%E6%89%93%E4%BA%A4%E9%81%93-dd420ccc7399)

[Bootstrap 常用 Layout](https://andy6804tw.github.io/2018/01/06/bootstrap-tutorial(1)/)



<div style="text-align: center">End</div>
-----------------------------------

![](https://i.imgur.com/888jFLr.gif)

<div style="text-align: right">2020.10.22</div>
