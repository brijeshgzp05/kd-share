$(document).ready(function(){
            var $myForm = $('.add-form')
            $myForm.submit(function(event){
                event.preventDefault()
                var $formData = $(this).serialize()
                var $endPoint = $myForm.attr('data-url') || window.location.href 
                $.ajax({
                    method: "POST",
                    url: $endPoint,
                    data: $formData,
                    beforeSend: function(){
                        $("#loading-overlay").show();
                    },
                    success: handleFormSuccess,
                    error: handleFormError,
                });

                    function handleFormSuccess(data, textStatus, jqXHR){
                        $("#loading-overlay").hide();
                    	var div = $('.error_block center');
                    	var div1 = $('.success_block center');
                        div.empty();
                        div1.empty();
                        console.log(data)
                        console.log(textStatus)
                        console.log(jqXHR)
                        $myForm[0].reset(); 

                        div1.append("<b>Request Sent</b><br>");
                    }

                    function handleFormError(jqXHR, textStatus, errorThrown){
                        $("#loading-overlay").hide();
                        var obj = jQuery.parseJSON( jqXHR.responseText );
                        var div = $('.error_block center');
                        var div1 = $('.success_block center');
                        div.empty();
                        div1.empty();
                        div.append("<p>"+obj["msg"]+"</p>")
                 

                        console.log(jqXHR)
                        console.log(textStatus)
                        console.log(errorThrown)
                    }
            });
         
        });