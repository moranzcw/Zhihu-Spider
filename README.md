# Zhihu-Spider

一个获取知乎用户主页信息的多线程Python爬虫程序。

简介：

* 使用[Requests](http://www.python-requests.org/en/master/)模拟HTTP请求/响应，[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)提取页面信息。
* 使用Python内置的Thread多线程和IP代理提升爬取速度，并绕过知乎的反爬虫机制。
* 使用Python内置的query作为消息队列。
* 用csv文件存储数据。

## 环境依赖

* beautifulsoup4
* requests

## 使用方法

在项目路径下输入以安装需要的模块：

```shell
$ pip install -r requirments.txt
```

运行：

```shell
$ python spider/run.py
```

## 数据

运行爬虫一段时间后，将会在项目目录下的datafile文件夹中找到存储数据的csv文件。

![](./image/datafilelist.png)

每个csv文件100MB，以方便数据分析，同时降低文件意外损坏带来的损失。

数据格式为典型的表格：

![](./image/datafile.png)

一共三列：

1. 第一列为用户的url token，如用户vczh的主页链接：https://www.zhihu.com/people/excited-vczh，那么vczh的token就是excited-vczh，用户token具有唯一性，适合作为程序中标识每个用户的ID。

2. 第二列为实际获取到的数据，数据是一个json，因为知乎在页面中是以json来传送用户信息的，所以我们直接存储这个json，这个json包含的信息很丰富，非常方便数据分析。

   比如整理格式后，用户vczh的json:

   ```json
   {
   	"isFollowed": false, 
   	"educations": 
   		[
   			{
   				"major": 
   					{
   						"url": "http://www.zhihu.com/api/v4/topics/19590324", 
   						"avatarUrl": "https://pic1.zhimg.com/e82bab09c_is.jpg", 
   						"name": "软件学院", 
   						"introduction": "", 
   						"type": "topic", 
   						"excerpt": "", 
   						"id": "19590324"
   					}, 
   				"school": 
   				{
   					"url": "http://www.zhihu.com/api/v4/topics/19599737", 
   					"avatarUrl": "https://pic2.zhimg.com/4d0d193a9_is.jpg", 
   					"name": "华南理工大学（SCUT）", 
   					"introduction": "华南理工大学（South China University of Technology）（原华南工学院，1952年建立）：教育部直属的重点大学，涵盖理、工、管、经、文、法等多学科，先后成为“211工程”和“985工程”院校，被誉为中国“南方工科大学的一面旗帜”，“工程师的摇篮”，“企业家的摇篮”。校园分为两个校区，北校区位于广州市天河区五山高校区，南校区位于广州市番禺区广州大学城内。学校占地面积4417亩(其中南校区1677亩)。北校区湖光山色交相辉映，绿树繁花香飘四季，民族式建筑与现代化楼群错落有致，环境优美清新，文化底蕴深厚，是教育部命名的“文明校园”；南校区是一个环境优美、设施先进、管理完善、制度创新的现代化校园，是莘莘学子求学的理想之地。", 
   					"type": "topic", 
   					"excerpt": "华南理工大学（South China University of Technology）（原华南工学院，1952年建立）：教育部直属的重点大学，涵盖理、工、管、经、文、法等多学科，先后成为“211工程”和“985工程”院校，被誉为中国“南方工科大学的一面旗帜”，“工程师的摇篮”，“企业家的摇篮”。校园分为两个校区，北校区位于广州市天河区五山高校区，南校区位于广州市番禺区广州大学城内。学校占地面积4417亩(其中南校区1677亩)。北校区湖光山色交相辉…", 
   					"id": "19599737"
   				}
   			}
   		], 
   	"followingCount": 2263, 
   	"voteFromCount": 0, 
   	"userType": "people", 
   	"showSinaWeibo": false, 
   	"pinsCount": 0, 
   	"isFollowing": false, 
   	"markedAnswersText": "编辑推荐", 
   	"isPrivacyProtected": false, 
   	"accountStatus": [], 
   	"isForceRenamed": false, 
   	"id": "0970f947b898ecc0ec035f9126dd4e08", 
   	"favoriteCount": 1, 
   	"voteupCount": 1388515, 
   	"commercialQuestionCount": 0, 
   	"isBlocking": false, 
   	"followingColumnsCount": 73, 
   	"headline": "专业造轮子，拉黑抢前排。gaclib.net", 
   	"urlToken": "excited-vczh", 
   	"participatedLiveCount": 6, 
   	"followingFavlistsCount": 20, 
   	"isAdvertiser": false, 
   	"isBindSina": true, 
   	"favoritedCount": 236566, 
   	"isOrg": false, 
   	"followerCount": 583782, 
   	"employments": 
   		[
   			{
   				"company": 
   					{
   						"url": "http://www.zhihu.com/api/v4/topics/19557307", 
   						"avatarUrl": "https://pic3.zhimg.com/v2-d3a9ee5ba3a2fe711087787c6169dcca_is.jpg", 
   						"name": "Microsoft Office", 
   						"introduction": "Microsoft Office 是一套由微软开发的办公软件。", 
   						"type": "topic", 
   						"excerpt": "Microsoft Office 是一套由微软开发的办公软件。", 
   						"id": "19557307"
   					}, 
   				"job": 
   					{
   						"url": "http://www.zhihu.com/api/v4/topics/19578588", 
   						"avatarUrl": "https://pic1.zhimg.com/e82bab09c_is.jpg", 
   						"name": "Developer", 
   						"introduction": "", 
   						"type": "topic", 
   						"excerpt": "", 
   						"id": "19578588"
   					}
   			}
   		], 
   	"type": "people", 
   	"avatarHue": "", 
   	"avatarUrlTemplate": "https://pic1.zhimg.com/3a6c25ac3864540e80cdef9bc2a73900_{size}.jpg", 
   	"followingTopicCount": 34, 
   	"description": "长期开发跨三大PC平台的GUI库<br><a href="https://link.zhihu.com/?target=http%3A//www.gaclib.net" class=" external" target="_blank" rel="nofollow noreferrer"><span class="invisible">http://www.</span><span class="visible">gaclib.net</span><span class="invisible"></span><i class="icon-external"></i></a>，讨论QQ群：231200072（不闲聊）<br>不再更新的技术博客：<a href="https://link.zhihu.com/?target=http%3A//www.cppblog.com/vczh" class=" external" target="_blank" rel="nofollow noreferrer"><span class="invisible">http://www.</span><span class="visible">cppblog.com/vczh</span><span class="invisible"></span><i class="icon-external"></i></a>", 
   	"business": 
   		{
   			"url": "http://www.zhihu.com/api/v4/topics/19619368", 
   			"avatarUrl": "https://pic1.zhimg.com/e82bab09c_is.jpg", 
   			"name": "计算机软件", 
   			"introduction": "徼", 
   			"type": "topic", 
   			"excerpt": "徼", 
   			"id": "19619368"
   		}, 
   	"avatarUrl": "https://pic1.zhimg.com/3a6c25ac3864540e80cdef9bc2a73900_is.jpg", 
   	"columnsCount": 5, 
   	"hostedLiveCount": 0, 
   	"isActive": 1, 
   	"thankToCount": 0, 
   	"mutualFolloweesCount": 0, 
   	"markedAnswersCount": 4, 
   	"coverUrl": "https://pic1.zhimg.com/v2-67b965aa94a92ed49b1a4205145b5cf4_b.jpg", 
   	"thankFromCount": 0, 
   	"voteToCount": 0, 
   	"isBlocked": false, 
   	"answerCount": 16163, 
   	"allowMessage": false, 
   	"articlesCount": 66, 
   	"name": "vczh", 
   	"questionCount": 487, 
   	"locations": 
   		[
   			{
   				"url": "http://www.zhihu.com/api/v4/topics/19583552", 
   				"avatarUrl": "https://pic4.zhimg.com/161f6ece791a4950ded3278fb74a2f9b_is.jpg", 
   				"name": "西雅图（Seattle）", 
   				"introduction": "西雅图是美国西北部最大的城市。多家高科技公司的总部（Microsoft, Amazon，Boeing 等等）坐落于此。", "type": "topic", 
   				"excerpt": "西雅图是美国西北部最大的城市。多家高科技公司的总部（Microsoft, Amazon，Boeing 等等）坐落于此。", 
   				"id": "19583552"
   			}
   		], 
   	"badge": [], 
   	"url": "http://www.zhihu.com/api/v4/people/0970f947b898ecc0ec035f9126dd4e08", 
   	"messageThreadToken": "4874924000", 
   	"logsCount": 2365, 
   	"followingQuestionCount": 26892, 
   	"thankedCount": 176110, 
   	"gender": 1
   }
   ```

   可以看到，用户vczh的教育信息，工作信息，描述，点赞数，被收藏数等等都被包含了。

3. 第三列保存每个用户的关注用户列表，每个用户只保存20个，此列不用作为数据，只作为爬虫中断后恢复现场和任务队列只用。分析数据时可以忽略。

## 程序机制
#### 程序结构
TODO

#### 代理

TODO

#### 用户信息获取
TODO

#### 数据存储
TODO

#### 并发
TODO