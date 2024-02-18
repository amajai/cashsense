(function($) {
	
	"use strict";
	
	/* Default Variables */
	var options = {
		loader:true,
		zoomControlDiv:null,
		rtl:false
	};
	
	if (typeof Naxos!=='undefined') {
		$.extend(options, Naxos);
	}
	
	$.project = {
		
		//Initialize
		init:function() {
			//RTL
			if ($('html').attr('dir')!=undefined && $('html').attr('dir')==='rtl') {
				options.rtl = true;
			}
			
			this.loader();
			this.animations();
			this.navigation();
			this.searchWrapper();
			this.scroll();
			this.smoothScroll();
			this.banner();
			this.lightBox();
			this.parallax();
            this.subscribe();
            this.contact();
			this.imageSlider();
			this.shortCodes();
		},
		
		//Page Loader
		loader:function() {
			if (options.loader) {
				$(window).on("load", function() {
					$(".page-loader").fadeOut();
				});
			}
		},
		
		//Animations
		animations:function() {
			new WOW().init();
		},
		
		//Navigation
		navigation:function() {
			//Dropdown menu
			$(".dropdown").on("click", function() {
                $(".submenu").slideToggle("slow");
			});
			
			//Mobile menu open
			$('.menu-bar').on("click", function() {
				$('.main-menu-area').addClass('mobile-menu-open');
			});

			//Mobile menu close
			$('.close-button').on("click", function() {
				$('.main-menu-area').removeClass('mobile-menu-open');
			});
		},
		
		//Search wrapper
		searchWrapper:function() {
			if ($('.search-option').length===0) {
				return;
			}
			
			var $search = $('.search-wrapper'),
				$searchIcon = $('.search-option'),
				$closeBtn = $('.search-close-btn');
			
			//Search button
			$searchIcon.on("click", function(e) {
				e.preventDefault();
				$search.addClass('wrapper-active');
			});

			//Close search window
			$closeBtn.on("click", function() {
				$search.removeClass('wrapper-active');
			});
		},
		
		//Scroll
		scroll:function() {
			$(window).on("scroll", function() {
				var pos = $(window).scrollTop();

				//Main menu scroll animation
				if (pos>=100) {
					$(".main-menu-area").addClass("fixed-menu slideInDown");
				} else {
					$(".main-menu-area").removeClass("fixed-menu slideInDown");
				}

				//Scroll to top button
				if (pos>=500) {
					$(".to-top").addClass("fixed-totop");
				} else {
					$(".to-top").removeClass("fixed-totop");
				}
			});
		},
		
		//Smooth scroll
		smoothScroll:function() {
			$('a.js-scroll-trigger[href*="#"]:not([href="#"])').on("click", function() {
				if (location.pathname.replace(/^\//, '')===this.pathname.replace(/^\//, '') && location.hostname===this.hostname) {
					var target = $(this.hash);
					target = target.length ? target : $('[name='+this.hash.slice(1)+']');
					
					if (target.length) {
						var pos = target.offset().top-30;
						$('html, body').animate({scrollTop:pos}, 100, 'easeInOutExpo');
						return false;
					}
				}
			});
			//Close responsive menu when a scroll trigger link is clicked
			$('.js-scroll-trigger').on('click', function() {
				$('.navbar-collapse').collapse('hide');
				$('.main-menu-area').removeClass('mobile-menu-open');
			});

			//Activate scrollspy to add active class to navbar items on scroll
			var active = $('a.js-scroll-trigger.active').attr("href");
			
			if (active !== undefined && active.startsWith("#")) {
				try {
					new bootstrap.ScrollSpy(document.body, {
						target:'#mainNav',
						offset:56
					});
				} catch(err) {}
			}
		},
		
		//Banner
		banner:function() {
			//Image background
			// if ($(".banner.image-bg").length>0) {
			// 	$(".banner.image-bg").backstretch("/static/images/banner/single-image.jpg");
			// }
			
			//Slide background
			if ($(".banner.slide-bg").length>0) {
				$(".banner.slide-bg").backstretch([
					"images/banner/slideshow-1.jpg", 
					"images/banner/slideshow-2.jpg", 
					"images/banner/slideshow-3.jpg"
				], {duration:3000, fade:750});
			}
			
			//Video background
			if ($(".banner.video-bg").length>0) {
				//Hide player on mobile
				if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
					$(".player").hide();
					$(".player-controls").hide();
				}

				//Youtube player
				$(".player").mb_YTPlayer();

				//Player controls
				$("#play").on("click", function() {
					$(".player").playYTP();
				});

				$("#pause").on("click", function() {
					$(".player").pauseYTP();
				});
			}
		},
		
		//Light box
		lightBox:function() {
			$('a[data-rel^=lightcase]').lightcase();
		},
		
		//Parallax sections
		parallax:function() {
			if ($('.parallax').length===0) {
				return;
			}
	
			$(window).on('load', function() {
				$('.parallax').each(function() {
					if ($(this).data('image')) {
						$(this).parallax('50%', 0.5);
						$(this).css({backgroundImage:'url('+$(this).data('image')+')'});
					}
				});
			});
		},
		
		//Background image
		bgImage:function() {
			if ($('.bg-img').length===0) {
				return;
			}
			
			$(window).on('load', function() {
				$('.bg-img').each(function() {
					if ($(this).data('image')) {
						$(this).css({backgroundImage:'url('+$(this).data('image')+')'});
					}
				});
			});
		},
        
        //Subscribe form
        subscribe:function() {
			if ($('#subscribe-form').length===0) {
				return;
			}
            
            var $subscribeForm = $("#subscribe-form");
            
            $subscribeForm.on('submit', function(e) {
				e.preventDefault();
                
                var email = $('.field-subscribe').val();

                //Validate email address
                if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                    var action = $subscribeForm.attr("action");
                    
                    $.ajax({
                        type:"POST",
                        url:action,
                        data:"email="+email,
                        dataType:"JSON",
                        success:function(data) {
                            if (data.status==="success") {
                                $subscribeForm[0].reset();
                                $("#subscribe-result").fadeIn();
                            } else {
								alert(data.type);
							}
                        }
                    });
                }
            });
        },
        
        //Contact form
        contact:function() {
			if ($('#contact-form').length===0) {
				return;
			}
            
            var $contactForm = $("#contact-form");
            
            var $name = $contactForm.find('.field-name'), 
                $email = $contactForm.find('.field-email'), 
                $subject = $contactForm.find('.field-subject'),
                $text = $contactForm.find('.field-message'), 
                $button = $contactForm.find('#contact-submit');

            $('.field-name, .field-email, .field-subject, .field-message').focus(function() {
                if ($(this).parent().find('.error').length>0) {
                    $(this).parent().find('.error').fadeOut(150, function() {
                        $(this).remove();
                    });
                }
            });
            
            $button.removeAttr('disabled');
            
            $contactForm.on('submit', function(e) {
				e.preventDefault();
            
                var fieldNotice = function($that) {
					if ($that.parent().find('.error').length===0) {
						$('<span class="error"><i class="fas fa-times"></i></span>').appendTo($that.parent()).fadeIn(150);
					}
				};
	
				if ($name.val().length<1) {fieldNotice($name);}
				if ($email.val().length<1) {fieldNotice($email);}
                if ($subject.val().length<1) {fieldNotice($subject);}
				if ($text.val().length<1) {fieldNotice($text);}
	
				if ($contactForm.find('span.error').length===0) {
					$(document).ajaxStart(function() {
						$button.attr('disabled', true);
					});
                    
                    var action = $contactForm.attr("action");
					
					$.post(action, {
						name:$name.val(), 
						email:$email.val(),
						subject:$subject.val(), 
						message:$text.val()
					}, function(response) {
						var data = $.parseJSON(response);
						
						if (data.status==='email') {
							fieldNotice($email);
							$button.removeAttr('disabled');
						} else if (data.status==='error') {
							$button.text('Unknown Error :(');
						} else {
							$('#contact-form').fadeOut();
							$('.contact-form-result').fadeIn();
						}
					});
				}
            });
        },
		
		//Image slider
		imageSlider:function($root, onComplete) {
			if (typeof $root==='undefined') {$root = $('body');}
			
			if ($root.find('.image-slider').length===0) {
				if (onComplete && typeof onComplete==='function') {onComplete();}
				return;
			}
			
			$root.find('.image-slider').each(function() {
				var $that = $(this), $arrows = $that.find('.arrows');
				var $list = $(this).find('> div').not('.arrows');
				var timeout, delay = false, process = false;
	
				var setHeight = function($that, onComplete) {
					$that.css({
						height:$that.find('> div:visible img').outerHeight(true)
					});
					
					if (onComplete && typeof onComplete==='function') {onComplete();}
				};
	
				if ($that.attr('data-delay')) {
					delay = parseInt($that.attr('data-delay'), 10);
					timeout = setInterval(function() {
						$arrows.find('.arrow.right').click();
					}, delay);
				}
	
				$(this).waitForImages(function() {
					$(this).css({position:'relative'});
	
					$list.hide().css({
						position:'absolute',
						top:0,
						left:0,
						zIndex:1,
						width:'100%',
						paddingLeft:15,
						paddingRight:15,
					});
	
					$list.eq(0).show();
	
					setHeight($that, onComplete);
					
					$(window).on('resize', function() {
						setTimeout(function() {
							setHeight($that);
						}, 1);
					});
	
					if ($list.length===1) {
						$arrows.hide();
						clearInterval(timeout);
						delay = false;
					}
				});
	
				$arrows.find('.arrow').on('click', function(e) {
					if (process) {
						e.preventDefault();
						return;
					}
					
					clearInterval(timeout);
	
					var isRight = $(this).hasClass('right');
					var $current = $that.find('> div:visible').not('.arrows'), $next;
	
					if (isRight) {
						$next = $current.next();
						if (!$next || $next.is('.arrows')) {
							$next = $list.eq(0);
						}
					} else {
						if ($current.is(':first-child')) {
							$next = $list.last();
						} else {
							$next = $current.prev();
						}
					}
	
					process = true;
					$current.css({zIndex:1});
					
					$next.css({opacity:0, zIndex:2}).show().animate({opacity:1}, {duration:300, queue:false, complete:function() {
						$current.hide().css({opacity:1});
						
						if (delay!==false) {
							timeout = setInterval(function() {
								$arrows.find('.arrow.right').click();
							}, delay);
						}
						process = false;
					}});
				});
			});
		},
		
		
		
		//Shortcodes
		shortCodes:function() {
			//Clients
			if ($('.clients-slider').length>0) {
				var dots = false;
				
				if ($('.clients-slider').data('dots')) {
					dots = true;
				}
				
				$('.clients-slider').owlCarousel({				
                    responsive:{
                        0:{
                            items:2
                        },
						576:{
                            items:3
                        },
                        768:{
                            items:5
                        }
                    },
					autoplay:3000,
                    autoplaySpeed:300,
					loop:true,
					dots:dots,
					dotsEach:2,
					rtl:options.rtl
                });
			}
			
			//Testimonials
            if ($('.testimonial-slider').length>0) {
				$(".testimonial-slider").slick({
					slidesToShow:1,
					slidesToScroll:1,
					arrows:false,
                    fade:true,
					asNavFor:".testimonial-nav",
					rtl:options.rtl
				});

				$(".testimonial-nav").slick({
					slidesToShow:5,
					slidesToScroll:1,
					asNavFor:".testimonial-slider",
                    arrows:false,
					centerMode:true,
					focusOnSelect:true,
					variableWidth:false,
					rtl:options.rtl,
                    responsive:[
						{
							breakpoint:991,
							settings:{
								slidesToShow:3,
                                arrows:false
							}
						},
						{
							breakpoint:480,
							settings:{
								slidesToShow:1,
                                arrows:false
							}
						}
					]
				});
			}
			
			//Counters
            if ($('.number-count').length>0) {
                $('.number-count').each(function() {
                    $(this).counterUp({
                        delay:4,
                        time:1000
                    });
                });                
			}
			
			//Screenshots
			if ($('.screenshot-slider').length>0) {
				var $screenshot = $('.screenshot-slider');
				
				$screenshot.owlCarousel({
					responsive:{
						0:{
							items:1
						},			 
						768:{
							items:2
						},			
						960 : {
							items:3
						}
					},
					responsiveClass:true,
					autoplay:true,
					autoplaySpeed:1000,
					loop:true,
					margin:30,
					dotsEach:2,
					rtl:options.rtl
				});
				
				if ($screenshot.hasClass('zoom-screenshot')) {
					$screenshot.magnificPopup({
						delegate:"a",
						type:"image",
						closeOnContentClick:false,
						closeBtnInside:false,
						mainClass:"mfp-with-zoom",
						image:{verticalFit:true},
						gallery:{enabled:true},
						zoom:{
							enabled:true,
							duration:300, // Don't forget to change the duration also in CSS
							opener:function(element) {
								return element.find("img");
							}
						}
					});
				}
			}
			
			//Skills
			if ($('.progress .progress-bar').length>0) {
				setTimeout(function() {
					$(window).scroll(function() {
						var scrollTop = $(window).scrollTop();

						$('.progress .progress-bar').each(function() {
							var $that = $(this), 
								itemTop = $that.offset().top-$(window).height()+$that.height()/2;

							if (scrollTop>itemTop && $that.outerWidth()===0) {
								var percent = parseInt($(this).attr('data-value'), 10)+'%';
								var $value = $(this).parent().parent().find('.progress-value');

								if ($value.length>0) {
									$value.css({width:percent, opacity:0}).html('<span>'+percent+'</span>');
								}

								$that.animate({width:percent}, {duration:1500, queue:false, complete:function() {
									if ($value.length>0) {
										$value.animate({opacity:1}, {duration:300, queue:false});
									}
								}});
							}
						});
					}).scroll();
				}, 1);
			}
		},
		
		//Share functions
		share:function(network, title, image, url) {
			//Window size
			var w = 650, h = 350, params = 'width='+w+', height='+h+', resizable=1';
	
			//Title
			if (typeof title==='undefined') {
				title = $('title').text();
			} else if (typeof title==='string') {
				if (title.indexOf("#")!=-1 && $(title).length>0) {
					title = $(title).text();
				}
			}
			
			title = title.trim();
			
			//Image
			if (typeof image==='undefined') {
				image = '';
			} else if (typeof image==='string') {
				if (!/http/i.test(image)) {
					if ($(image).length>0) {
						if ($(image).is('img')) {
							image = $(image).attr('src');
						} else {
							image = $(image).find('img').eq(0).attr('src');
						}
					} else {
						image = '';
					}
				}
			}
			
			//Url
			if (typeof url==='undefined') {
				url = document.location.href;
			} else {
				url = document.location.protocol+'//'+document.location.host+document.location.pathname+url;
			}
		
			
			return;
		}
		
	};
	
	//Initialize
	$.project.init();

	$('.sidebar-toggle').on("click", function() {
		let sidemenu = document.querySelector('.sidemenu')
		sidemenu.classList.toggle('show');
	});

})(jQuery);



