#encoding=utf-8
from math import sqrt
critics={'Lisa Rose':{'Lady in the water':2.5,'Snakes on a Plane':3.5,'Just My Luck':3.0,'Superman Return':3.5,'You,Me and Dupree':2.5,'The Night Listener':3.0},'Gene Seymour':{'Lady in the water':3.0,'Snakes on a Plane':3.5,'Just My Luck':1.5,'Superman Return':5.0,'You,Me and Dupree':3.5,'The Night Listener':3.0},'Michael Phillips':{'Lady in the water':2.5,'Snakes on a Plane':3.0,'Just My Luck':3.0,'Superman Return':3.5,'The Night Listener':4.0},'Claudia Puig':{'Snakes on a Plane':3.5,'Just My Luck':3.0,'Superman Return':4.0,'The Night Listener':4.5,'You,Me and Dupree':2.5},'Mick Lasalle':{'Lady in the water':3.0,'Snakes on a Plane':4.0,'Just My Luck':2.0,'Superman Return':3.0,'You,Me and Dupree':2.0,'The Night Listener':3.0},'Jack Matthews':{'Lady in the water':3.0,'Snakes on a Plane':4.0,'Just My Luck':3.0,'Superman Return':5.0,'You,Me and Dupree':3.5,'The Night Listener':3.0},'Toby':{'Snakes on a Plane':4.5,'Superman Return':4.0,'You,Me and Dupree':1.0}}
#欧几里德距离计算用户的相似度，返回一个[0,1]值
#计算方法：将两个user对喜欢的每个物品的评分求差并平方，然后相加，最后求平方
def sim_distance(prefs,p1,p2):
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
    if len(si)==0:
        return 0;

    sum_of_squares=sum(pow(prefs[p1][item]-prefs[p2][item],2) for item in prefs[p1] if item in prefs[p2])

    return 1/(1+sqrt(sum_of_squares))
#皮尔孙相关度计算用户相似度，返回[-1,1]
#计算方法：
def sim_pearson(prefs,p1,p2):
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
    n=len(si)
    if n==0:
        return 1

    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])

    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==n:return 0
    r=num/den
    return r

def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

// START USER OMIT
def getRecommedations(prefs,person,similarity=sim_pearson):
    totals={};simSums={}
    #遍历每一个用户
    for other in prefs:
        #遍历到的用户是当前用户，跳过
        if other==person:continue
        #不是当前用户，计算用户之间的相似度
        sim=similarity(prefs,person,other)
        if sim<=0:continue
        #遍历用户的物品
        for item in prefs[other]:
            #如果当前用户没有评价该物品
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)
                #评价值与用户相似度加权 // HL
                totals[item]+=prefs[other][item]*sim
                simSums.setdefault(item,0)
                #相似度和
                simSums[item]+=sim
    #对相似度归一化
    rankings=[(total/simSums[item],item) for item,total in totals.items()]
    #排序，降序，返回结果
    rankings.sort();rankings.reverse()
    return rankings
// END USER OMIT

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person]=prefs[person][item]
    return result
def calculateSimilarItems(prefs,n=10):
    # 建立字典，以为出与这些物品最为相近的所有其他物品
    result={}

    #以物品为中心对偏好矩阵实施倒置处理
    itemPrefs=transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        #针对大数据集更新状态变量
        c+=1
        if c%100==0:
            print "%d / %d" %(c,len(itemPrefs))
            #寻找最为相近的物品
        scores=topMatches(itemPrefs,item,n,similarity=sim_distance)
        result[item]=scores
    return result
// START ITEM OMIT
def getRecommedationedItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}
    #遍历当前用户评论过的物品
    for(item,rating) in userRatings.items():
        #遍历每一个物品
        for(similarity,item2) in itemMatch[item]:
            #如果item2用户评论过，跳过
            if item2 in userRatings:continue
            #评价值与物品相似度的加权之和 // HL
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            #相似度和
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
    #对相似度归一化
    rankings=[(score/totalSim[item],item) for item,score in scores.items()]
    #排序，降序，返回结果
    rankings.sort()
    rankings.reverse()
    return rankings
// END ITEM OMIT
if __name__ == '__main__':
      #print sim_pearson(critics,'Lisa Rose','Gene Seymour')
    #print [(p,topMatches(critics,p,6,sim_distance)) for p in critics]
    persons_cf=[(p,getRecommedations(critics,p)) for p in critics]
    print "=========基于用户的协同过滤推荐列表========="
    for p,items in persons_cf:
        if len(items)==0:continue
        print "%s:%s" % (p,items)
    print "=========基于物品的协同过滤推荐列表========="
    #movies=transformPrefs(critics)
    itemMatchs=calculateSimilarItems(critics)
    items_cf= [(p,getRecommedationedItems(critics,itemMatchs,p)) for p in critics]
    for p,items in items_cf:
        if len(items)==0:continue
        print "%s:%s" % (p,items)
    #print [(m,topMatches(movies,m,6)) for m in movies] 
