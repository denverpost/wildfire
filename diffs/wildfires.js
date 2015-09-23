// Publish a list of recent fires.
// Also create an object that manages a map and allows us to view all
// the available fire boundaries.

// One fire looks like this:
// {
//     "state": "CO",
//     "fire": "Rifle Range",
//     "slug": "CO-GRX-J2LD",
//     "datetime": "2015-08-25 10:44:00.000000",
//     "url": "http://rmgsc.cr.usgs.gov/outgoing/GeoMAC/current_year_fire_data/KMLS/CO-GRX-J2LD%20Rifle%20Range%208-25-2015%201044.kml"
// }

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



var mapmanager = {
    slugify: function (str) {
        // From http://dense13.com/blog/2009/05/03/converting-string-to-slug-javascript/
        str = str.replace(/^\s+|\s+$/g, ''); // trim
        str = str.toLowerCase();

        // remove accents, swap ñ for n, etc
        var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
        var to   = "aaaaeeeeiiiioooouuuunc------";
        for (var i=0, l=from.length ; i<l ; i++) {
            str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
        }

        str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

        return str;
    },
    map: L.map('map', { zoomControl:true }).setView([39.7392, -104.8847], 7),
    info: L.control(),
    layerOptions: L.geoJson(null, {
        //filter: function(item) {
        //    return true;
        //},
        onEachFeature: function (feature, layer) {
/*
            var slug = window.choropleth.slugify(feature['properties']['NBHD_NAME']);
            //console.log(feature, layer);
            //layer.on("hover", function(e) { console.log('ahs'); });
            layer.on({
                click: function(e) { window.location.href = '/neighborhood/' + slug; },
                mouseover: function(e)
                {
                    window.choropleth.info.update(this.feature.properties);                   
                },
                mouseout: function(e) 
                { 
                    window.choropleth.info.update(); 
                }
            });
*/
        },
        // http://leafletjs.com/reference.html#geojson-style
        style: function(feature) {
            return { 
                weight: 1,
                color: '#f00' 
            };
        }
    }),
    init: function() {
        L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
        }).addTo(this.map);
        var runlayer = omnivore.kml("output/CO/CO-LSD-JYZ9_Red_Dirt_7-20-2015_1400.kml", null, this.layerOptions)
            .on("ready", function(e) 
            {
                console.log(e);
                var points = [];
                var keys = Object.keys(runlayer._layers);
                var count = keys.length;
                for ( var i = 0; i < count; i++ )
                {
                    if ( typeof runlayer._layers[keys[i]]._latlng !== "undefined" )
                    {
                        points.push(runlayer._layers[keys[i]]._latlng); 
                    }
                }
                window.mapmanager.map.fitBounds(points);
                window.mapmanager.map.zoomOut(6);
            }).addTo(this.map);

        // Functions that control the on-hover info windows
        this.info.options = {
            position: 'bottomright'
        };
        this.info.onAdd = function (map) {
            this._div = L.DomUtil.create('div', 'info');
            this.update();
            return this._div;
        };
        this.info.update = function (props) {
/*
            if ( typeof props !== 'undefined' )
            {
                var slug = window.choropleth.slugify(props['NBHD_NAME']);
            }
            this._div.innerHTML =  (props ?  '<h2>' + props['NBHD_NAME'] + '</h2>' 
                : 'Hover over a neighborhood');
*/
        };
        this.info.addTo(this.map);
    }
};
mapmanager.init();
