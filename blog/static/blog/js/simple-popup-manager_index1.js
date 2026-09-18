jQuery(function () {
  var popups_list = jQuery('.simple-popup-manager');
  if (popups_list.length) {
    popups_list.each(function (index, popup) {
      popup = jQuery(popup);
      var when_display = popup.data('when-display');
      var when_hide = popup.data('when-hide');
      switch (when_display) {
        case 'exit':
          show_on_exit_intend(popup)
          break;
        case 'begin_scroll':
          on_scroll(popup, 'begin');
          break;
        case 'middle_scroll':
          on_scroll(popup, 'middle');
          break;
        case 'end_scroll':
          on_scroll(popup, 'end');
          break;
        default:
          show_after_x_seconds(popup, when_display);
      }
      switch (when_hide) {
        case 'never':
          break;
        case 'begin_scroll':
          on_scroll(popup, 'begin', 'hide');
          break;
        case 'middle_scroll':
          on_scroll(popup, 'middle', 'hide');
          break;
        case 'end_scroll':
          on_scroll(popup, 'end', 'hide');
          break;
        default:
          hide_after_x_seconds(popup, when_hide);
      }
    });
  }

  var popups_close_button = jQuery('.simple-popup-manager-close-btn');
  if (popups_close_button.length) {
    popups_close_button.on('click', function (event) {
      event.preventDefault();
      var popup = jQuery(this).parents('.simple-popup-manager');
      close_popup(popup)
      return false;
    });
  }

  function display_popup(popup) {
    if (popup.hasClass('simple-popup-manager-visible')) {
      return false;
    }
    var popup_id = popup.data('id');
    if (get_redisplay_time(popup_id)) {
      return false;
    }

    popup.addClass('simple-popup-manager-visible');
    var type = popup.data('type');
    switch (type) {
      case 'bar':
        push_content_down(popup);
        break;
    }
  }

  function show_after_x_seconds(popup, seconds) {
    setTimeout(display_popup, seconds * 1000, popup);
  }

  function hide_after_x_seconds(popup, seconds) {
    seconds = parseInt(seconds);
    if (seconds < 1) {
      return false;
    }
    setTimeout(close_popup, seconds * 1000, popup);
  }

  function on_scroll(popup, when = 'begin', action = 'show') {
    var document_height = jQuery(document).height();
    var window_height = jQuery(window).height();
    var full_height = document_height - window_height;
    var user_scrolled, scroll_percent;
    var scroll_listener = debounce(function () {
      user_scrolled = jQuery(window).scrollTop();
      scroll_percent = Math.floor((user_scrolled * 100) / full_height);
      if (when === 'begin' && scroll_percent > 10) {
        action === 'show' ? display_popup(popup) : close_popup(popup);
      } else if (when === 'middle' && scroll_percent > 40) {
        action === 'show' ? display_popup(popup) : close_popup(popup);
      } else if (when === 'end' && scroll_percent > 80) {
        action === 'show' ? display_popup(popup) : close_popup(popup);
      }
    }, 200);
    jQuery(document).on('scroll', scroll_listener);
  }

  function show_on_exit_intend(popup) {
    jQuery(document).on('mouseleave', function () {
      display_popup(popup);
    });
  }

  function close_popup(popup) {
    var redisplay_after = popup.data('redisplay-after');
    var popup_id = popup.data('id');
    if (redisplay_after === 'never') {
      set_redisplay_time(popup_id, 365);
    } else if (redisplay_after === 'every_page_load') {

    } else {
      set_redisplay_time(popup_id, redisplay_after);
    }
    if (popup.data('type') === 'bar') {
      push_content_back(popup);
    }
    popup.removeClass('simple-popup-manager-visible')
  }

  function set_redisplay_time(popup_id, redisplay_after) {
    redisplay_after = parseInt(redisplay_after);
    if (redisplay_after > 0) {
      var redisplay_after_seconds = now() + (redisplay_after * 86400)
      localStorage.setItem(popup_id + '__simple_popup_manager_display_after', redisplay_after_seconds.toString())
    }
  }

  function get_redisplay_time(popup_id) {
    var redisplay_after_seconds = parseInt(localStorage.getItem(popup_id + '__simple_popup_manager_display_after'));
    if (redisplay_after_seconds > now()) {
      return redisplay_after_seconds;
    }
    return 0;
  }

  function push_content_down(popup) {
    var bar = popup.find('.spm_bar');
    var height = bar.outerHeight();
    var admin_bar = jQuery('#wpadminbar');
    var admin_bar_height = 0
    if (admin_bar.length) {
      admin_bar_height = admin_bar.outerHeight();
      height = height + admin_bar_height;
      bar.css('margin-top', admin_bar_height + 'px');
    }
    if (popup.data('push-content-down')) {
      jQuery('html').attr('style', function (i, s) {
        return (s || '') + ';margin-top:' + height + 'px !important;'
      });
    }
  }

  function push_content_back(popup) {
    var admin_bar = jQuery('#wpadminbar');
    var height = 0;
    if (admin_bar.length) {
      height = admin_bar.outerHeight();
    }
    if (popup.data('push-content-down')) {
      jQuery('html').attr('style', function (i, s) {
        return (s || '') + ';margin-top:' + height + 'px !important;'
      });
    }
  }

  function now() {
    return Math.floor(Date.now() / 1000);
  }

  /**
   *
   * Returns a function, that, as long as it continues to be invoked, will not
   * be triggered. The function will be called after it stops being called for
   * N milliseconds. If `immediate` is passed, trigger the function on the
   * leading edge, instead of the trailing.
   *
   * @param func
   * @param wait
   * @param immediate
   * @returns {(function(): void)|*}
   */
  function debounce(func, wait, immediate) {
    var timeout;
    return function () {
      var context = this, args = arguments;
      var later = function () {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      var callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
    };
  }

  function get_current_breakpoint() {
    var browser_width = $(window).width();
    if (browser_width <= 768 && browser_width >= 481) {
      return 'tablet';
    } else if (browser_width <= 480) {
      return 'mobile'
    } else {
      return 'desktop'
    }
  }
});


