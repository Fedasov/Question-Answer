const centrifuga = document.getElementsByClassName('channel')
const ws_url = centrifuga[0].dataset.ws_url
const token = centrifuga[0].dataset.token
const channel = centrifuga[0].dataset.channel
const url_avatar = centrifuga[0].dataset.url_avatar


const centrifuge = new Centrifuge(ws_url, {
  token: token
});

centrifuge.on('connecting', function (ctx) {
  console.log(`connecting: ${ctx.code}, ${ctx.reason}`);
}).on('connected', function (ctx) {
  console.log(`connected over ${ctx.transport}`);
}).on('disconnected', function (ctx) {
  console.log(`disconnected: ${ctx.code}, ${ctx.reason}`);
}).connect();

const sub = centrifuge.newSubscription(channel);

sub.on('publication', function (ctx) {
    console.log(ctx);
    console.log(url_avatar);
    div.insertAdjacentHTML("beforeend", `<div class="answer row">
             <div class="col-3">
                    <img src="${ ctx.data.url_avatar }" class="question-image" alt="...">
                 <div class="reaction-answer">
                    <button type="button" data-id="${ ctx.data.id }" data-like="True" class="btn btn-light">
                        <i class="bi bi-hand-thumbs-up"></i>
                    </button>
                    <span>${ ctx.data.rating }</span>
                    <button type="button" data-id="${ ctx.data.id }" data-like="False" class="btn btn-light">
                        <i class="bi bi-hand-thumbs-down"></i>
                    </button>
                 </div>
            </div>

             <div class="col-9 correct-checkpoint">
                <div><p>${ ctx.data.content }</p></div>
                <? if (request.user.id == ctx.data.user.id): ?>
                     <div class="fluency correct-answer form-check">
                        <? if (ctx.data.correct): ?>
                            <input class="form-check-input" data-id="${ ctx.data.id }" type="checkbox" checked>
                        <? else: ?>
                            <input class="form-check-input" data-id="${ ctx.data.id }" type="checkbox">
                        <? endif; ?>
                        <label class="form-check-label">
                            Correct!
                        </label>
                         <? if (ctx.data.correct): ?>
                            <div class="fs-2 mb-3">
                                <i class="bi bi-check"></i>Correct!
                            </div>
                         <? endif; ?>
                     </div>
                <? endif; ?>
            </div>
        </div>
    `);
}).on('subscribing', function (ctx) {
  console.log(`subscribing: ${ctx.code}, ${ctx.reason}`);
}).on('subscribed', function (ctx) {
  console.log('subscribed', ctx);
}).on('unsubscribed', function (ctx) {
  console.log(`unsubscribed: ${ctx.code}, ${ctx.reason}`);
}).subscribe();