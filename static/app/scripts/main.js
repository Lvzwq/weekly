$(document).ready(function(){
    var select = $('#weekly-select');
    var newspaperWrap = $('.weekly__newspaper-container');
    var blocksWrap = $('.weekly__newspaper-mask');
    var newsBlocks = [];
    var newspaperContainer = $('#newspaper-container');
    var newspaper = $('#newspaper');
    var contentWrap = $('#content');
    var contentNavList = $('#navlist');
    var curPaper;

    function Block(index,top,left,width,height,title,id){
        this.index = index;
        this.top = top;
        this.left = left;
        this.width = width;
        this.height = height;
        this.title = title;
        this.setElem = function(){
            var block = $('<div></div>');
            block.attr('id','newsblock' + index);
            block.addClass('weekly__newsblock');
            block.append('<div data-aid="'+id+'" class="weekly__newsblock-info"><span class="weekly__newsblock-triangle"></span>'+title+'</div>');
            block.css({
                top: top,
                left: left,
                width: width,
                height: height
            });
            blocksWrap.append(block);
        }
    }

    select.on('change',function(){
        var news = select.val();
        loadNav(news);
        $.ajax('loadnewspaper',{
            type: 'POST',
            data: {
                news: news
            }
        })
            .done(function(data){
                data = JSON.parse(data);
                if(data.code == 1){
                    newsBlocks = [];
                    blocksWrap.empty();
                    var blocks = data.blocks;
                    curPaper = data.newspaper_num;
                    newspaperContainer.empty().append('<img id="newspaper" class="weekly__newspaper-img" src="'+data.newspaper_url+'" alt=""/>');
                    for (var i = 0,length = blocks.length; i < length; i++){
                        var newBlock = new Block(blocks[i].index,blocks[i].top,blocks[i].left,blocks[i].width,blocks[i].height,blocks[i].title);
                        newBlock.setElem();
                        newsBlocks.push(newBlock);
                    }
                }
            })
    });

    blocksWrap.on('click','.weekly__newsblock',function(){
        loadArticle($(this).data('aid'));
    });

    function loadArticle(data){
        contentWrap.empty().append('<div class="weekly__content-loading">正在加载。。。</div>');
        if(data){
            $.ajax('xxx',{
                type: 'GET',
                data: {
                    news: curPaper,
                    article: data
                }
            })
                .done(function(data){
                    data = JSON.parse(data);
                    if(data.code == 1){
                        var HTML = '<span id="goback1" class="weekly__content-goback"> 返回 </span>' +
                            '<article class="weekly__content-article">' +
                            data.article +
                            '</article>' +
                            '<span id="goback2" class="weekly__content-goback"> 返回 </span>';
                        contentWrap.empty();
                        contentWrap.append(HTML);
                    }
                });
        }
    }
    function loadList(data){

    }
    function loadNav(data){

    }
});
