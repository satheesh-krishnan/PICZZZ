document.getElementById('follow').onclick=function(){
            this.disabled =true
            imagename = document.getElementById('image').alt
            followstatus = this.value
            
            $.get('/piczzz/followpic',{iname:imagename,followstats:followstatus},function(follownumbers){
            rdata = JSON.parse(follownumbers)
            follownum = rdata["follownum"]
            
            if (followstatus == 'follow'){
                document.getElementById('follow').disabled = false
                document.getElementById('follow').value = 'unfollow'
                if (follownum == 1){document.getElementById('follownumber').innerHTML = follownum+' follower'}
                else {document.getElementById('follownumber').innerHTML = follownum+' followers'}}
            else if(followstatus == 'unfollow'){
                document.getElementById('follow').disabled = false
                document.getElementById('follow').value = 'follow'
                if (follownum == 1){document.getElementById('follownumber').innerHTML = follownum+' follower'}
                else {document.getElementById('follownumber').innerHTML = follownum+' followers'}}
          
})}

document.getElementById('comment').onclick=function(){
            imagename = document.getElementById('image').alt
            commenttext = document.getElementById('commenttext').value
	    $.get('/piczzz/comments',{iname:imagename,commentvalue:commenttext},function(commentnumbers){
            rdata = JSON.parse(commentnumbers)
            commentnums = rdata["commentnum"]
            if (commentnums == ''){}
            else{if(commentnums == 1){document.getElementById('commentnumber').innerHTML = commentnums+' comment'}
            else{document.getElementById('commentnumber').innerHTML = commentnums+' comments'}
            newcommentdiv = document.createElement('div')
            cname = rdata['cname']
            datedata = rdata['datedata']
            cmid = rdata["commentid"]
            document.getElementById('commenttext').value=''
            document.getElementById('newcommentcontainer').innerHTML='<div id=nn'+cmid+' style="color:#0ac;">'+cname+'</div><div id=d'+cmid+'>'+commenttext+'<div><input type="button" value="edit"  id='+cmid+' onClick="handlecomment(this.id,this.value)"><input type="button" value="delete"  id='+cmid+' onClick="handlecomment(this.id,this.value)"></div></div><div id=dd'+cmid+'>'+datedata+'</div></br></br>'
             
            if (commentnums == 2){
document.getElementById('comdiv').innerHTML += '<meta id="commentpagenumber" content="1"><div id="commentcontainer"></div><input type="submit" id="loadcomment" value="load comments" onClick="loadcomnt()">'}
             }      
            
            
})}

document.getElementById('loadcomment').onclick = function(){
          imagename = document.getElementById('image').alt
          commentpageno = document.getElementById('commentpagenumber').content
          $.get('/piczzz/loadcomments',{iname:imagename,commentpagenumber:commentpageno},function(commentlist){
                rdata =JSON.parse(commentlist)
                if (rdata['commentlist']){
                   for (data in rdata['commentlist']){
                   dat = rdata['commentlist'][data]
                   if(dat['sameuser']){
                   document.getElementById('commentcontainer').innerHTML+='<div id=nn'+dat['comid']+' style="color:#0ac;">'+dat['comname']+'</div><div id=d'+dat['comid']+'>'+dat['comtext']+'<div><input type="button" value="edit"  id='+dat['comid']+' onClick="handlecomment(this.id,this.value)"><input type="button" value="delete"  id='+dat['comid']+' onClick="handlecomment(this.id,this.value)"></div></div><div id=dd'+dat['comid']+'>'+dat['datedata']+'</div></br></br>'              
}
                   else if(dat['samepic']){document.getElementById('commentcontainer').innerHTML+='<div id=nn'+dat['comid']+' style="color:#0ac;">'+dat['comname']+'</div><div id=d'+dat['comid']+'>'+dat['comtext']+'<div><input type="button" value="delete" id='+dat['comid']+' onClick="handlecomment(this.id,this.value)"></div></div><div id=dd'+dat['comid']+'>'+dat['datedata']+'</div></br></br>'}
                   else{document.getElementById('commentcontainer').innerHTML+='<div id=nn'+dat['comid']+' style="color:#0ac;">'+dat['comname']+'</div><div id=d'+dat['comid']+'>'+dat['comtext']+'<div id=dd'+dat['comid']+'>'+dat['datedata']+'</div></div></br></br>'}} 
document.getElementById('commentpagenumber').content = parseInt(commentpageno)+1
if (rdata["lastflag"]){document.getElementById('loadcomment').style.visibility="hidden"}
}})}

function handlecomment(clkid,clkvalue){
if (clkvalue == "edit"){ 
      textvalue =document.getElementById('d'+clkid).textContent
      htmlback = document.getElementById('d'+clkid).innerHTML
      document.getElementById('d'+clkid).innerHTML='<textarea id=t'+clkid+'>'+textvalue+'</textarea><div><input type="button" value="save" id=s'+clkid+'><input type="button" value="cancel" id=c'+clkid+'></div>'
document.getElementById('s'+clkid).onclick=function(){
 newcontent = document.getElementById('t'+clkid).value
 if (newcontent){
 $.get('/piczzz/editcomment',{clickid:clkid,textcontent:newcontent,optionto:"edit"},function(result){
           resdata = JSON.parse(result)
           
           if (resdata["changed"]){
           
           document.getElementById('d'+clkid).innerHTML = '<div id=d'+clkid+'>'+resdata['textcon']+'<div><input type="button" value="edit"  id='+clkid+' onClick="handlecomment(this.id,this.value)"><input type="button" value="delete"  id='+clkid+' onClick="handlecomment(this.id,this.value)"></div></div>'
           document.getElementById('dd'+clkid).innerHTML='<div id=dd'+dat['comid']+'>'+resdata['date']+'</div></br></br>'}
           
else{document.getElementById('d'+clkid).innerHTML=htmlback}                                          
})}
else{alert("nothing to save")
document.getElementById('d'+clkid).innerHTML=htmlback}



}

document.getElementById('c'+clkid).onclick=function(){
document.getElementById('d'+clkid).innerHTML=htmlback
}
}
else if(clkvalue="delete"){
$.get('/piczzz/editcomment',{clickid:clkid,optionto:"delete"},function(commentnums){

comrdata = JSON.parse(commentnums)

commentnumbers = comrdata["commentnum"]
ele1 = document.getElementById('nn'+clkid)
ele2 = document.getElementById('d'+clkid)
ele3 = document.getElementById('dd'+clkid)
ele1.parentNode.removeChild(ele1)
ele2.parentNode.removeChild(ele2)
ele3.parentNode.removeChild(ele3)

if(parseInt(commentnumbers) == 1){document.getElementById('commentnumber').innerHTML = commentnumbers+' comment'}
            else{document.getElementById('commentnumber').innerHTML = commentnumbers+' comments'}

})
}
}



function loadcomnt(){
          imagename = document.getElementById('image').alt
          commentpageno = document.getElementById('commentpagenumber').content
          $.get('/piczzz/loadcomments',{iname:imagename,commentpagenumber:commentpageno},function(commentlist){
                rdata =JSON.parse(commentlist)
                if (rdata['commentlist']){
                   rdata['commentlist'].shift()
                   for (data in rdata['commentlist']){
                   dat = rdata['commentlist'][data]
                   if(dat['sameuser']){
                   document.getElementById('commentcontainer').innerHTML+='<div id=nn'+dat['comid']+' style="color:#0ac;">'+dat['comname']+'</div><div id=d'+dat['comid']+'>'+dat['comtext']+'<div><input type="button" value="edit"  id='+dat['comid']+' onClick="handlecomment(this.id,this.value)"><input type="button" value="delete"  id='+dat['comid']+' onClick="handlecomment(this.id,this.value)"></div></div><div id=dd'+dat['comid']+'>'+dat['datedata']+'</div></br></br>'              
}
                   else if(dat['samepic']){document.getElementById('commentcontainer').innerHTML+='<div id=nn'+dat['comid']+' style="color:#0ac;">'+dat['comname']+'</div><div id=d'+dat['comid']+'>'+dat['comtext']+'<div><input type="button" value="delete" id='+dat['comid']+' onClick="handlecomment(this.id,this.value)"></div></div><div id=dd'+dat['comid']+'>'+dat['datedata']+'</div></br></br>'}
                   else{document.getElementById('commentcontainer').innerHTML+='<div id=nn'+dat['comid']+' style="color:#0ac;">'+dat['comname']+'</div><div id=d'+dat['comid']+'>'+dat['comtext']+'<div id=dd'+dat['comid']+'>'+dat['datedata']+'</div></div></br></br>'}} 
document.getElementById('commentpagenumber').content = parseInt(commentpageno)+1
if (rdata["lastflag"]){document.getElementById('loadcomment').style.visibility="hidden"}
}})}
