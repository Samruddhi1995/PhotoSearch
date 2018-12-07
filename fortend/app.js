
var apigClient = apigClientFactory.newClient();



var apigClient = apigClientFactory.newClient({
  apiKey: '-------------'
});

var resultdiv = $('#results');

function previewFile(){
       var file    = document.querySelector('input[type=file]'); //sames as here
       var reader = new FileReader();

        //sendpicture(file.files[0])
    
      

       result1 = ValidateSize(file)
       result2 = isImage(file.files[0])
       
       reader.readAsDataURL(file.files[0]);

       if (result1 === 1 && result2 === 1){
      reader.addEventListener("load", function() {
        ImageURL = reader.result;
        var block = ImageURL.split(";");
        var realData = block[1].split(",")[1];
        sendpicture_1(realData) 
      }) 

      function sendpicture_1(realData){
        //console.log(file.files[0])
        sendpicture(realData,file.files[0])
      }}
  }

 function ValidateSize(file) {
        var FileSize = file.files[0].size / 1024 / 1024; // in MB
        if (FileSize > 15) {
            alert('File size exceeds 15 MB');
           // $(file).val(''); //for clearing with Jquery
        } else {
            return 1
        }
    }

function isImage(filename) {
    var ext = filename.type;
    console.log(ext)
    switch (ext.toLowerCase()) {
    case 'image/png':
    case 'image/jpeg':
        return 1;
    }
    alert('Please upload png or jpeg format only')
   
}

function sendpicture(body,file){
  console.log("body")
  console.log(body)
  var params = {
  // This is where any modeled request parameters should be added.
  // The key is the parameter name, as it is defined in the API in API Gateway.
  'item': file.name,
  'folder': 'assign3-s3-triggers-lambda',
  'Content-Type': "text/plain"
};
  


var additionalParams = {
  'Content-Type': "text/plain"
};

apigClient.uploadFolderItemPut(params, body=body, additionalParams)
    .then(function(result){
      console.log(result.status)
      if (result.status == 200) {
        alert('Image uploaded successfully')
      }
      else{
        alert("There was error while uploading image please try again")
      }
    }).catch( function(result){
       alert("There was error while uploading image please try again")
    });
}


$(".mytext").on("keyup", function(e){
    if (e.which == 13){
        var text = $(this).val();
        if (text !== ""){
            console.log(text); 
            querry = text
            searchimage(querry)
            $(this).val('');
        }
    }
});

function searchimage(querry){
  var params = {
  // This is where any modeled request parameters should be added.
  // The key is the parameter name, as it is defined in the API in API Gateway.
  'q': querry
};
  

var body = {};
var additionalParams = {
  'Access-Control-Allow-Origin': '*'
};

apigClient.searchGet(params, body, additionalParams)
    .then(function(result){
      console.log(result.data)
      display(result)
    }).catch( function(result){

    });
}


function display(result){

  if(result.data === "No such search results!"){
    alert("No such search results!")
  }
  else if(result.data === "Inappropiate Querry"){
    console.log("Here")
    alert("Inappropiate Querry")
  }
  else{
     console.log("Here in 3")
     console.log(result.data)
     console.log(result.data.results)
     console.log(result.data.results.length)
     var i;
     for (i = 0; i < result.data.results.length; i++) { 
       console.log(result.data.results[i])
       labels = result.data.results[i].labels
       url = result.data.results[i].url
       console.log(url)
       resultdiv.append('<div class="result">' +
          '<img src='+url+'>' +
          '<div><h2>'+labels+'</h2><p>');
        }

       }
  
}


