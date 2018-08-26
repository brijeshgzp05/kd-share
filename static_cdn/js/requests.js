$(document).ready(function(){
        $('.add').click(function(){
            document.location.href = "{% url  'friend:add' %}"
        });
        $('button').click(function(){
        	curr = $(this);
        	if(curr.hasClass("can") || curr.hasClass("rej")){

        		var endpoint = "{% url 'friend:del' pk=123 %}"
        		endpoint = endpoint.replace('123',this.id)
        		
        		$.ajax({
                    method: "GET",
                    url: endpoint,

                    data: "",
                    beforeSend: function(){
                        $("#loading-overlay").show();
                    },
                    success: function(data, textStatus, jqXHR){
                    	$("#loading-overlay").hide();
                    	var tr = curr.parent().parent();
                    	tr.hide();
                    	alert(data["message"]);

                    },
                    error: function(){
                    	$("#loading-overlay").hide();
                    	alert("Failed due to some reasons")
                    },
                });

        	}
        	else if(curr.hasClass("acc")){
        		var endpoint = "{% url 'friend:acc' pk=123 %}"
        		endpoint = endpoint.replace('123',this.id)
        		
        		$.ajax({
                    method: "GET",
                    url: endpoint,

                    data: "",
                    beforeSend: function(){
                        $("#loading-overlay").show();
                    },
                    success: function(data, textStatus, jqXHR){
                    	$("#loading-overlay").hide();
                    	var tr = curr.parent().parent();
                    	tr.hide();
                    	alert(data["message"]);

                    },
                    error: function(){
                    	$("#loading-overlay").hide();
                    	alert("Failed due to some reasons")
                    },
                });
        	}
        });

         
    });