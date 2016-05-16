document.getElementById('followpeople').onclick=function(){
            username = document.getElementById('username').textContent
            followstatus = this.value
            
            $.get('/piczzz/followpeople',{uname:username,followstats:followstatus},function(follownumbers){
            rdata = JSON.parse(follownumbers)
            following = rdata["following"]
            followers = rdata["followers"]
            
            if (followstatus == 'follow'){
                document.getElementById('followpeople').value = 'unfollow'
                document.getElementById('following').innerHTML = 'following '+following
                document.getElementById('followers').innerHTML = 'followers '+followers}
            else if(followstatus == 'unfollow'){
                document.getElementById('followpeople').value = 'follow'
                document.getElementById('following').innerHTML = 'following '+following
                document.getElementById('followers').innerHTML = 'followers '+followers }
})}
