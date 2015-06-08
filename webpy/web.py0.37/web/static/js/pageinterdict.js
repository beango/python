$(function() { 
    $(document).get(0).oncontextmenu = function() {
        return false;
    };
    
    $(document).get(0).onselectstart = function() {
        return false;
    };
    
    $(document).keydown(function(event){
        if(event.keyCode == 123) {
            event.preventDefault();
            return false;
        }
    });
});