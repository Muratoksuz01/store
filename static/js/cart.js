var updatebtns=document.getElementsByClassName('update-cart')
for( var i=0;i<updatebtns.length;i++){
    updatebtns[i].addEventListener('click',function(){
        var productid=this.dataset.product
        var action=this.dataset.action
        console.log("productid:",productid,"action",action)
        console.log("USER",user)
        if (user=="AnonymousUser"){
            console.log("the user not authenticated")
        }
        else{
            updateUserOrder(productid,action)        
        }
        
    })
}

function updateUserOrder(productid, action) {
    console.log("the user authenticated");
    var url = "/update_item/";
    fetch(url, {
      method: "post",
      headers: { "Content-type": "application/json",'X-CSRFToken':csrftoken },
      body: JSON.stringify({ 'productid': productid, 'action': action }),
    })
      .then((response) => response.json())
      .then((data) => {

    })
    location.reload();
     
  }



