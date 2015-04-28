
 window.fbAsyncInit = function() {
  FB.init({
    appId      : '1565760477011269',
    cookie     : true,  // enable cookies to allow the server to access the session BASE.HTML
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.3' 
  });
  FB.Event.subscribe('auth.login', function (response) {
      //where redirect occurs upon login (also occurs if user not fb logged in refreshes page after being logged in) (needs to stay as is)
      console.log('fb.event.subscribe 1; response:'+JSON.stringify(response));
      window.location = "http://bullpostcorbin.herokuapp.com";
 });

  FB.getLoginStatus(function(response) {
    //statusChangeCallback(response);
      if (response.status === 'connected') {
          statusChangeCallback(response);
      }else{
        console.log('user is not logged into facebook ');
        window.location = "http://bullpostcorbin.herokuapp.com/logout/";
      } 
  });

  //  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&appId=1565760477011269&version=v2.3";

  // This is called with the results from from FB.getLoginStatus().
  function statusChangeCallback(response) {
    console.log('fb.getAuthResponse:'+FB.getAuthResponse.accessToken);
    console.log(response);
    // defines current login status of the person
    if (response.status === 'connected') {
      console.log('user is logged in');

            //vars for innerHTML assignment
            var name;
            var age;
            var locale;            
            var profilePic = document.createElement('img');

            //grabs user name and birthday 
            FB.api(
                "/me",
                function (response) {
                  if (response && !response.error) {
                   console.log('Successful login for: ' + response.name);
                   console.log('users birthday:'+response.birthday);    
                   document.getElementById('status').innerHTML = 'Thanks for logging in, ' + response.name + '!';
                   
                   //age calculation script
                    function agefinding()
                     {
                        var birthDay = response.birthday;
                        var DOB = new Date(birthDay);
                        var today = new Date();
                        var ageCalc = today.getTime() - DOB.getTime();
                        ageCalc = Math.floor(ageCalc / (1000 * 60 * 60 * 24 * 365.25));
                        return ageCalc;
                    }                  
                  if(response.birthday != 'undefined'){
                    age = agefinding();
                    console.log('age:'+agefinding());
                  }else{
                    age = 'age not found';
                    console.log('cant find age');
                  }
                  
                  name = response.name;
                  locale = response.locale;
                  profilePic.src = 'https://graph.facebook.com/'+response.id+'/picture?width=200';
                               
                  var profileName = document.getElementById("profileName");
                  var profileLocale = document.getElementById("profileLocale");
                  var profilePicture= document.getElementById("profilePicture");
                  var profileAge= document.getElementById("profileAge");
 
                  profilePicture.appendChild(profilePic);                   
                  profileName.innerHTML = name;
                  profileLocale.innerHTML = locale;
                  profileAge.innerHTML = age+" years old";
                }                
            });

          var location = "unkown";
          FB.api("/me/location",
            function(response) {
              if (response && !response.error) {
                location = response.data;
              }
              var profileLocation = document.getElementById("profileLocation");
              profileLocation.innerHTML = location;
              console.log('fb. api location of user:'+JSON.stringify(response));
              //for empty path (before facebook review) return is: {"error":{"message":"Unknown path components: /about_me","type":"OAuthException","code":2500}}"
            }
          );
          
          var bio = "unset bio";
          FB.api("/me/about_me",
            function(response) {
              if (response && !response.error) {
                bio = response.data;
              }
              var profileBio = document.getElementById("profileBio");
              profileBio.innerHTML = bio;
              console.log('user about me:'+JSON.stringify(response));
              //for empty path return is: {"error":{"message":"Unknown path components: /about_me","type":"OAuthException","code":2500}}"
            }
          );
           FB.api("/me/permissions",
            function(response) {
              console.log('permissions requests length:'+response.data.length);
            }
          );
          FB.api("/me/friends",
            function(response) {
              console.log('friends using app:'+JSON.stringify(response.data));
            }
          );

          var friendsIDarray = [];
          var user_friends_list;
          var friendPic= document.createElement('img');
          
          FB.api("/me/taggable_friends?fields=id,name,picture.type(large)",
            function(response) {
              console.log('taggable_friends length:'+response.data.length);
              if (response && !response.error) {
                var numberOfTaggableFriends = response.data.length;
                if (response.data.length > 0) {
                  for (var i = 0; i < numberOfTaggableFriends; i++) {
                     var data = response.data;
                     //console.log('data ID of person:'+data[i].id+'; name of person:'+data[i].name+'; friends profile picture:'+data[i].picture.data.url);
                     friendsIDarray.push(data[i].id);
                  }
                  user_friends_list = friendsIDarray.join();
                  console.log('user_friends_list [length]:'+user_friends_list.length);
                  return;
                }else{
                  console.log('taggable_friends data array is empty');
                }
              }              
          });
          
          
    }else if (response.status === 'not_authorized') {
      console.log('person is logged into FB but not app');
      // The person is logged into Facebook, but not your app.
      document.getElementById('status').innerHTML = 'Please log into FriendSpeak.';
    } else {
      // The person is not logged into Facebook; unsure if logged into app or not.
      console.log('person not logged into FB or app; FB.login starting');
          FB.login(function(response) {
            //taggable_friends,user_about_me,user_birthday,user_location
            // handle the response {"authResponse":null,"status":"unknown"} when exit out of dialog box
            console.log('FB.login response handling: this was where strinfigy response happened');
          }, {scope: 'public_profile', 
            return_scopes: true
            }
          );
      document.getElementById('status').innerHTML = 'Please log into Facebook.';
    }
  }
};