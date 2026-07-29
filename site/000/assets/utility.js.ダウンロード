var _____WB$wombat$assign$function_____=function(name){return (globalThis._wb_wombat && globalThis._wb_wombat.local_init && globalThis._wb_wombat.local_init(name))||globalThis[name];};if(!globalThis.__WB_pmw){globalThis.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opener = _____WB$wombat$assign$function_____("opener");
jQuery(function(){

//マウスオーバー（ファイルの末尾に「_off」「_on」で切り替え）
jQuery("img.over,input.over")
.each( function(){
	jQuery("<img>,<input>").attr("src",jQuery(this).attr("src").replace(/^(.+)_off(\.[a-z]+)$/, "$1_on$2"));
})
.mouseover( function(){
	jQuery(this).attr("src",jQuery(this).attr("src").replace(/^(.+)_off(\.[a-z]+)$/, "$1_on$2"));
})
.mouseout( function(){
	jQuery(this).attr("src",jQuery(this).attr("src").replace(/^(.+)_on(\.[a-z]+)$/, "$1_off$2"));
});

//検索ボックス内のテキスト
jQuery(".search").val("検索ワードを入力");
jQuery(".search").focus( function(){
	var searchWord=jQuery(this);
		if(searchWord.val()=='検索ワードを入力'){
		jQuery(this).val(""),
		jQuery(this).addClass("onfocus");
	};
});
jQuery(".search").blur( function(){
	var searchWord=jQuery(this);
		if(searchWord.val()==''){
		jQuery(this).val("検索ワードを入力"),
		jQuery(this).removeClass("onfocus");
	};
});

//テーブルのセルとリストに偶数・奇数を付与
jQuery("li:odd,tr:odd").addClass("odd"),
jQuery("li:even,tr:even").addClass("even");

//スムーズスクロール
jQuery("a[href^=#]").click(function(){
	var Hash = jQuery(this.hash);
	var HashOffset = jQuery(Hash).offset().top;
	jQuery("html,body").animate({
		scrollTop: jQuery(jQuery(this).attr("href")).offset().top }, 'slow','swing');
	return false;
});

//グローバルメニューのプルダウン設定
jQuery("#menu li").hover(function() {
	jQuery("> ul:not(:animated)", this).fadeIn("normal");
}, function() {
	jQuery("> ul", this).fadeOut("normal");
});


//グローバルメニュー用のIE「z-index」バグ対策
var zNum = 1000;
jQuery('#global-nav li').each(function() {
	jQuery(this).css('zIndex', zNum);
	zNum = zNum-10;
});

//モバイル用のグローバルメニュー設定
jQuery(".btn-gnav").click(function(){
	jQuery(".menu-wrap").toggleClass("showMenu");
});

//モバイル用のサイドバーとサブコンテンツの設定
jQuery(".sub-contents-btn").click(function(){
	jQuery(".sub-column #sub-contents-in").toggleClass("showSubConts");
});

jQuery(".sidebar-btn").click(function(){
	jQuery(".sub-column #sidebar-in").toggleClass("showSidebar");
});

//クリックでテキストを選択
jQuery(".text-field")
	.focus(function(){
		jQuery(this).select();
	})
	.click(function(){
		jQuery(this).select();
		return false;
});


});



}

/*
     FILE ARCHIVED ON 06:21:33 Sep 29, 2017 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 03:28:53 Jul 29, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  capture_cache.get: 3.387
  load_resource: 221.961
  PetaboxLoader3.resolve: 55.001
  PetaboxLoader3.datanode: 15.186
*/