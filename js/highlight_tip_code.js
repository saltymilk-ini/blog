function highlight_tip_code() {
    document.addEventListener('DOMContentLoaded', function () {
        setTimeout(function () {
            const codeBlocks = document.querySelectorAll('.main-area pre code');

            codeBlocks.forEach(function (block) {
                block.innerHTML = block.innerHTML.replace(
                    /\{\{tip-code\}\}(.*?)\{\{\/tip-code\}\}/g,
                    '<span class="tip-code">$1</span>'
                );
            });
        }, 300);
    });
}