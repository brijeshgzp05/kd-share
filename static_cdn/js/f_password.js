$(document).ready(function(){
        var $myForm = $('.verify-form')
        $myForm.submit(function(event){
            event.preventDefault()
            var $formData = $(this).serialize()
            var $endPoint = $myForm.attr('data-url') || window.location.href // or set your own url
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
                	document.location.href = "{% url 'accounts:code' %}"
                    
                }

                function handleFormError(jqXHR, textStatus, errorThrown){
                	$("#loading-overlay").hide();
                	var obj = jQuery.parseJSON( jqXHR.responseText );
					$('#error_block').text(obj.email)
                    console.log(jqXHR)
                    console.log(textStatus)
                    console.log(errorThrown)
                }
        });
     
        

    });