$.ajax({
    dataType: 'json',
    //url: 'http://extras.denverpost.com/app/trial-results/output/config.jsonp',
    url: 'output/CO-fires.json',
    success: function (items) 
    {
        console.log(items); 
        $.each(items, function(item) 
        {
            var fire = items[item];
            $('#fires').append('<li>' + fire['fire'] + '</li>');
        });
    }
});
