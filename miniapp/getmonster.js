var FileSaver = require('file-saver'); 

 let data = {
          name:"hanmeimei",
          age:88
      }
var content = JSON.stringify(data);

var blob = new Blob([content ], {type: "text/plain;charset=utf-8"}); 

FileSaver.saveAs(blob, "hello world.txt");

