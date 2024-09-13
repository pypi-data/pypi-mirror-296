(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[8593],{13687:function(e,i,t){(window.__NEXT_P=window.__NEXT_P||[]).push(["/privacy-requests/configure/messaging",function(){return t(38917)}])},43124:function(e,i,t){"use strict";t.d(i,{Z:function(){return m}});var n=t(24246),s=t(13054),r=t(88038),l=t.n(r),a=t(86677);t(27378);var o=t(11596),c=t(72247),u=t(11032),d=()=>{let e=(0,a.useRouter)();return(0,n.jsx)(s.xuv,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,n.jsxs)(s.xuv,{children:[(0,n.jsxs)(s.Kqy,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,n.jsx)(s.xvT,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,n.jsx)(s.zxk,{size:"sm",variant:"outline",onClick:()=>{e.push(u.fz)},children:"Configure"})]}),(0,n.jsxs)(s.xvT,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})},m=e=>{let{children:i,title:t,padded:r=!0,mainProps:u}=e,m=(0,o.hz)(),x=(0,a.useRouter)(),h="/privacy-requests"===x.pathname||"/datastore-connection"===x.pathname,p=!(m.flags.privacyRequestsConfiguration&&h),{data:f}=(0,c.JE)(void 0,{skip:p}),{data:g}=(0,c.PW)(void 0,{skip:p}),v=m.flags.privacyRequestsConfiguration&&(!f||!g)&&h;return(0,n.jsxs)(s.kCb,{"data-testid":t,direction:"column",h:"100vh",children:[(0,n.jsxs)(l(),{children:[(0,n.jsxs)("title",{children:["Fides Admin UI - ",t]}),(0,n.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,n.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,n.jsxs)(s.kCb,{as:"main",direction:"column",py:r?6:0,px:r?10:0,h:r?"calc(100% - 48px)":"full",flex:1,minWidth:0,overflow:"auto",...u,children:[v?(0,n.jsx)(d,{}):null,i]})]})}},60136:function(e,i,t){"use strict";t.d(i,{D4:function(){return r.D4},MM:function(){return m},Ot:function(){return c},c6:function(){return s},cj:function(){return h},e$:function(){return a},fn:function(){return o},iC:function(){return x},nU:function(){return d},tB:function(){return u}});var n,s,r=t(41164);let l="An unexpected error occurred. Please try again.",a=function(e){let i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:l;if((0,r.Bw)(e)){if((0,r.hE)(e.data))return e.data.detail;if((0,r.cz)(e.data)){var t;let i=null===(t=e.data.detail)||void 0===t?void 0:t[0];return"".concat(null==i?void 0:i.msg,": ").concat(null==i?void 0:i.loc)}if(409===e.status&&(0,r.Dy)(e.data)||404===e.status&&(0,r.XD)(e.data))return"".concat(e.data.detail.error," (").concat(e.data.detail.fides_key,")")}return i};function o(e){return"object"==typeof e&&null!=e&&"status"in e}function c(e){return"object"==typeof e&&null!=e&&"data"in e&&"string"==typeof e.data.detail}function u(e){return"object"==typeof e&&null!=e&&"data"in e&&Array.isArray(e.data.detail)}let d=function(e){let i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{status:500,message:l};if((0,r.oK)(e))return{status:e.originalStatus,message:e.data};if((0,r.Bw)(e)){let{status:t}=e;return{status:t,message:a(e,i.message)}}return i},m=e=>Object.entries(e).map(e=>({value:e[1],label:e[1]}));(n=s||(s={})).GVL="gvl",n.AC="gacp",n.COMPASS="compass";let x={gvl:{label:"GVL",fullName:"Global Vendor List"},gacp:{label:"AC",fullName:"Google Additional Consent List"},compass:{label:"",fullName:""}},h=e=>{let i=e.split(".")[0];return"gacp"===i?"gacp":"gvl"===i?"gvl":"compass"}},65399:function(e,i,t){"use strict";t.d(i,{HK:function(){return r},VY:function(){return n.V},O3:function(){return a}});var n=t(75139),s=t(60136);let r=()=>{let{errorAlert:e}=(0,n.V)();return{handleError:i=>{let t="An unexpected error occurred. Please try again.";(0,s.Ot)(i)?t=i.data.detail:(0,s.tB)(i)&&(t=i.data.detail[0].msg),e(t)}}};var l=t(27378);let a=e=>{let i=(0,l.useRef)(void 0);return(0,l.useEffect)(()=>{let t=t=>{var n;(null===(n=i.current)||void 0===n?void 0:n.contains(t.target))||e()};return document.addEventListener("mousedown",t),()=>{document.removeEventListener("mousedown",t)}},[i,e]),{ref:i}}},75139:function(e,i,t){"use strict";t.d(i,{V:function(){return r}});var n=t(24246),s=t(13054);let r=()=>{let e=(0,s.pmc)();return{errorAlert:(i,t,r)=>{let l={...r,position:(null==r?void 0:r.position)||"top",render:e=>{let{onClose:r}=e;return(0,n.jsxs)(s.bZj,{alignItems:"normal",status:"error",children:[(0,n.jsx)(s.zMQ,{}),(0,n.jsxs)(s.xuv,{children:[t&&(0,n.jsx)(s.CdC,{children:t}),(0,n.jsx)(s.XaZ,{children:i})]}),(0,n.jsx)(s.PZ7,{onClick:r,position:"relative",right:0,size:"sm",top:-1})]})}};(null==r?void 0:r.id)&&e.isActive(r.id)?e.update(r.id,l):e(l)},successAlert:(i,t,r)=>{let l={...r,position:(null==r?void 0:r.position)||"top",render:e=>{let{onClose:r}=e;return(0,n.jsxs)(s.bZj,{alignItems:"normal",status:"success",variant:"subtle",children:[(0,n.jsx)(s.zMQ,{}),(0,n.jsxs)(s.xuv,{children:[t&&(0,n.jsx)(s.CdC,{children:t}),(0,n.jsx)(s.XaZ,{children:i})]}),(0,n.jsx)(s.PZ7,{onClick:r,position:"relative",right:0,size:"sm",top:-1})]})}};(null==r?void 0:r.id)&&e.isActive(r.id)?e.update(r.id,l):e(l)}}}},73485:function(e,i,t){"use strict";t.d(i,{R:function(){return a}});var n=t(24246),s=t(13054),r=t(79894),l=t.n(r);let a=e=>{let{onClick:i,...t}=e;return(0,n.jsxs)(s.kCb,{alignItems:"center",mt:-4,mb:3,onClick:i,cursor:"pointer",...t,children:[(0,n.jsx)(s.hU,{"aria-label":"Back",icon:(0,n.jsx)(s.Rpv,{}),mr:2,size:"xs",variant:"outline"}),(0,n.jsx)(s.xvT,{as:"a",fontSize:"sm",fontWeight:"500",children:"Back"})]})};i.Z=e=>{let{backPath:i,...t}=e;return(0,n.jsxs)(s.kCb,{alignItems:"center",mb:6,...t,children:[(0,n.jsx)(s.hU,{as:l(),href:i,"aria-label":"Back",icon:(0,n.jsx)(s.Rpv,{}),mr:2,size:"xs",variant:"outline"}),(0,n.jsx)(s.xvT,{as:l(),href:i,fontSize:"sm",fontWeight:"500",children:"Back"})]})}},95758:function(e,i,t){"use strict";t.d(i,{DE:function(){return a},MP:function(){return s},qX:function(){return l},rE:function(){return r}});var n=t(19686);let s=new Map([[n.q2.APPROVED,"Approved"],[n.q2.CANCELED,"Canceled"],[n.q2.COMPLETE,"Completed"],[n.q2.DENIED,"Denied"],[n.q2.ERROR,"Error"],[n.q2.IN_PROCESSING,"In Progress"],[n.q2.PENDING,"New"],[n.q2.PAUSED,"Paused"],[n.q2.IDENTITY_UNVERIFIED,"Unverified"],[n.q2.REQUIRES_INPUT,"Requires input"]]),r=new Map([[n.Us.ACCESS,"Access"],[n.Us.ERASURE,"Erasure"],[n.Us.CONSENT,"Consent"],[n.Us.UPDATE,"Update"]]),l={mailgun:"mailgun",twilio_email:"twilio_email",twilio_text:"twilio_text"},a={local:"local",s3:"s3"}},38917:function(e,i,t){"use strict";t.r(i),t.d(i,{default:function(){return y}});var n=t(24246),s=t(13054),r=t(27378),l=t(60136),a=t(65399),o=t(43124),c=t(73485),u=t(11032),d=t(95758),m=t(72247),x=t(34090),h=t(34803),p=e=>{let{messagingDetails:i}=e,{successAlert:t}=(0,a.VY)(),{handleError:r}=(0,a.HK)(),[o]=(0,m.SU)(),c=i.service_type===d.qX.twilio_email||i.service_type===d.qX.mailgun,u=i.service_type===d.qX.twilio_text,p=async e=>{if(c){let i=await o({email:e.email});(0,l.D4)(i)?r(i.error):t("Test message successfully sent.")}if(u){let i=await o({phone_number:e.phone});(0,l.D4)(i)?r(i.error):t("Test message successfully sent.")}};return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(s.izJ,{mt:10}),(0,n.jsx)(s.X6q,{fontSize:"md",fontWeight:"semibold",mt:10,mb:5,children:"Test connection"}),(0,n.jsx)(s.Kqy,{children:(0,n.jsx)(x.J9,{initialValues:{email:"",phone:""},onSubmit:p,children:e=>{let{isSubmitting:i,resetForm:t}=e;return(0,n.jsxs)(x.l0,{children:[c?(0,n.jsx)(h.j0,{name:"email",label:"Email",placeholder:"youremail@domain.com",isRequired:!0}):null,u?(0,n.jsx)(h.j0,{name:"phone",label:"Phone",placeholder:"+10000000000",isRequired:!0}):null,(0,n.jsxs)(s.xuv,{mt:10,children:[(0,n.jsx)(s.zxk,{onClick:()=>t(),mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,n.jsx)(s.zxk,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})})]})},f=()=>{var e;let{successAlert:i}=(0,a.VY)(),[t,o]=(0,r.useState)(""),{handleError:c}=(0,a.HK)(),{data:u}=(0,m.S3)({type:d.qX.mailgun}),[f]=(0,m.h9)(),[g]=(0,m.iI)(),v=async e=>{let t=await f({service_type:d.qX.mailgun,details:{is_eu_domain:"false",domain:e.domain}});(0,l.D4)(t)?c(t.error):(i("Mailgun email successfully updated. You can now enter your security key."),o("apiKey"))},j=async e=>{let t=await g({details:{mailgun_api_key:e.api_key},service_type:d.qX.mailgun});(0,l.D4)(t)?c(t.error):(i("Mailgun security key successfully updated."),o("testConnection"))},y={domain:null!==(e=null==u?void 0:u.details.domain)&&void 0!==e?e:""};return(0,n.jsxs)(s.xuv,{children:[(0,n.jsx)(s.X6q,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Mailgun messaging configuration"}),(0,n.jsx)(s.Kqy,{children:(0,n.jsx)(x.J9,{initialValues:y,onSubmit:v,enableReinitialize:!0,children:e=>{let{isSubmitting:i,handleReset:t}=e;return(0,n.jsxs)(x.l0,{children:[(0,n.jsx)(s.Kqy,{mt:5,spacing:5,children:(0,n.jsx)(h.j0,{name:"domain",label:"Domain",placeholder:"Enter domain","data-testid":"option-twilio-domain",isRequired:!0})}),(0,n.jsxs)(s.xuv,{mt:10,children:[(0,n.jsx)(s.zxk,{onClick:t,mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,n.jsx)(s.zxk,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})}),"apiKey"===t||"testConnection"===t?(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(s.izJ,{mt:10}),(0,n.jsx)(s.X6q,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Security key"}),(0,n.jsx)(s.Kqy,{children:(0,n.jsx)(x.J9,{initialValues:{api_key:""},onSubmit:j,children:e=>{let{isSubmitting:i,handleReset:t}=e;return(0,n.jsxs)(x.l0,{children:[(0,n.jsx)(h.j0,{name:"api_key",label:"API key",type:"password",isRequired:!0}),(0,n.jsxs)(s.xuv,{mt:10,children:[(0,n.jsx)(s.zxk,{onClick:t,mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,n.jsx)(s.zxk,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})})]}):null,"testConnection"===t?(0,n.jsx)(p,{messagingDetails:u||{service_type:d.qX.mailgun}}):null]})},g=()=>{var e;let[i,t]=(0,r.useState)(""),{successAlert:o}=(0,a.VY)(),{handleError:c}=(0,a.HK)(),{data:u}=(0,m.S3)({type:d.qX.twilio_email}),[f]=(0,m.h9)(),[g]=(0,m.iI)(),v=async e=>{let i=await f({service_type:d.qX.twilio_email,details:{twilio_email_from:e.email}});(0,l.D4)(i)?c(i.error):(o("Twilio email successfully updated. You can now enter your security key."),t("configureTwilioEmailSecrets"))},j=async e=>{let i=await g({details:{twilio_api_key:e.api_key},service_type:d.qX.twilio_email});(0,l.D4)(i)?c(i.error):(o("Twilio email secrets successfully updated."),t("testConnection"))},y={email:null!==(e=null==u?void 0:u.details.twilio_email_from)&&void 0!==e?e:""};return(0,n.jsxs)(s.xuv,{children:[(0,n.jsx)(s.X6q,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Twilio Email messaging configuration"}),(0,n.jsx)(s.Kqy,{children:(0,n.jsx)(x.J9,{initialValues:y,onSubmit:v,enableReinitialize:!0,children:e=>{let{isSubmitting:i,handleReset:t}=e;return(0,n.jsxs)(x.l0,{children:[(0,n.jsx)(s.Kqy,{mt:5,spacing:5,children:(0,n.jsx)(h.j0,{name:"email",label:"Email",placeholder:"Enter email",isRequired:!0})}),(0,n.jsxs)(s.xuv,{mt:10,children:[(0,n.jsx)(s.zxk,{onClick:()=>t(),mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,n.jsx)(s.zxk,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})}),"configureTwilioEmailSecrets"===i||"testConnection"===i?(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(s.izJ,{mt:10}),(0,n.jsx)(s.X6q,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Security key"}),(0,n.jsx)(s.Kqy,{children:(0,n.jsx)(x.J9,{initialValues:{api_key:""},onSubmit:j,children:e=>{let{isSubmitting:i,handleReset:t}=e;return(0,n.jsxs)(x.l0,{children:[(0,n.jsx)(s.Kqy,{mt:5,spacing:5,children:(0,n.jsx)(h.j0,{name:"api_key",label:"API key",type:"password",isRequired:!0})}),(0,n.jsxs)(s.xuv,{mt:10,children:[(0,n.jsx)(s.zxk,{onClick:()=>t(),mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,n.jsx)(s.zxk,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})})]}):null,"testConnection"===i?(0,n.jsx)(p,{messagingDetails:u||{service_type:d.qX.twilio_email}}):null]})},v=()=>{let{successAlert:e}=(0,a.VY)(),{handleError:i}=(0,a.HK)(),[t,o]=(0,r.useState)(""),{data:c}=(0,m.S3)({type:"twilio_text"}),[u]=(0,m.iI)(),f=async t=>{let n=await u({details:{twilio_account_sid:t.account_sid,twilio_auth_token:t.auth_token,twilio_messaging_service_sid:t.messaging_service_sid,twilio_sender_phone_number:t.phone},service_type:d.qX.twilio_text});(0,l.D4)(n)?i(n.error):(e("Twilio text secrets successfully updated."),o("testConnection"))};return(0,n.jsxs)(s.xuv,{children:[(0,n.jsx)(s.X6q,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Twilio SMS messaging configuration"}),(0,n.jsx)(s.Kqy,{children:(0,n.jsx)(x.J9,{initialValues:{account_sid:"",auth_token:"",messaging_service_sid:"",phone:""},onSubmit:f,enableReinitialize:!0,children:e=>{let{isSubmitting:i,handleReset:t}=e;return(0,n.jsxs)(x.l0,{children:[(0,n.jsxs)(s.Kqy,{mt:5,spacing:5,children:[(0,n.jsx)(h.j0,{name:"account_sid",label:"Account SID",placeholder:"Enter account SID",isRequired:!0}),(0,n.jsx)(h.j0,{name:"auth_token",label:"Auth token",placeholder:"Enter auth token",type:"password",isRequired:!0}),(0,n.jsx)(h.j0,{name:"messaging_service_sid",label:"Messaging Service SID",placeholder:"Enter messaging service SID"}),(0,n.jsx)(h.j0,{name:"phone",label:"Phone Number",placeholder:"Enter phone number"})]}),(0,n.jsxs)(s.xuv,{mt:10,children:[(0,n.jsx)(s.zxk,{onClick:()=>t(),mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,n.jsx)(s.zxk,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})}),"testConnection"===t?(0,n.jsx)(p,{messagingDetails:c||{service_type:d.qX.twilio_text}}):null]})},j=()=>{let{successAlert:e}=(0,a.VY)(),{handleError:i}=(0,a.HK)(),[t,x]=(0,r.useState)(""),[h]=(0,m.h9)(),[p]=(0,m.L)(),{data:j}=(0,m.JE)();(0,r.useEffect)(()=>{j&&x(null==j?void 0:j.service_type)},[j]);let y=async t=>{let n=await p({notifications:{notification_service_type:t,send_request_completion_notification:!0,send_request_receipt_notification:!0,send_request_review_notification:!0},execution:{subject_identity_verification_required:!0}});if((0,l.D4)(n))i(n.error);else if(t!==d.qX.twilio_text)x(t);else{let n=await h({service_type:d.qX.twilio_text});(0,l.D4)(n)?i(n.error):(e("Messaging provider saved successfully."),x(t))}};return(0,n.jsxs)(o.Z,{title:"Configure Privacy Requests - Messaging",children:[(0,n.jsx)(c.Z,{backPath:u.fz}),(0,n.jsx)(s.X6q,{mb:5,fontSize:"2xl",fontWeight:"semibold",children:"Configure your messaging provider"}),(0,n.jsxs)(s.xuv,{display:"flex",flexDirection:"column",width:"50%",children:[(0,n.jsxs)(s.xuv,{children:["Fides requires a messsaging provider for sending processing notices to privacy request subjects, and allows for Subject Identity Verification in privacy requests. Please follow the"," ",(0,n.jsx)(s.xvT,{as:"span",color:"complimentary.500",children:"documentation"})," ","to setup a messaging service that Fides supports. Ensure you have completed the setup for the preferred messaging provider and have the details handy prior to the following steps."]}),(0,n.jsx)(s.X6q,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Choose service type to configure"}),(0,n.jsx)(s.FXm,{onChange:y,value:t,"data-testid":"privacy-requests-messaging-provider-selection",colorScheme:"secondary",p:3,children:(0,n.jsxs)(s.Kqy,{direction:"row",children:[(0,n.jsx)(s.Y8K,{value:d.qX.mailgun,"data-testid":"option-mailgun",mr:5,children:"Mailgun Email"},d.qX.mailgun),(0,n.jsx)(s.Y8K,{value:d.qX.twilio_email,"data-testid":"option-twilio-email",children:"Twilio Email"},d.qX.twilio_email),(0,n.jsx)(s.Y8K,{value:d.qX.twilio_text,"data-testid":"option-twilio-sms",children:"Twilio SMS"},d.qX.twilio_text)]})}),t===d.qX.mailgun?(0,n.jsx)(f,{}):null,t===d.qX.twilio_email?(0,n.jsx)(g,{}):null,t===d.qX.twilio_text?(0,n.jsx)(v,{}):null]})]})},y=()=>(0,n.jsx)(j,{})},41164:function(e,i,t){"use strict";t.d(i,{Bw:function(){return l},D4:function(){return s},Dy:function(){return o},XD:function(){return c},cz:function(){return u},hE:function(){return a},oK:function(){return r}});var n=t(76649);let s=e=>"error"in e,r=e=>(0,n.Ln)({status:"string"},e)&&"PARSING_ERROR"===e.status,l=e=>(0,n.Ln)({status:"number",data:{}},e),a=e=>(0,n.Ln)({detail:"string"},e),o=e=>(0,n.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),c=e=>(0,n.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),u=e=>(0,n.Ln)({detail:[{loc:["string","number"],msg:"string",type:"string"}]},e)},76649:function(e,i,t){"use strict";t.d(i,{Ln:function(){return n},uX:function(){return l}});let n=(e,i)=>r(e,i),s=Symbol("SOME"),r=(e,i)=>"string"==typeof e?e===typeof i:Array.isArray(e)?s in e?e.some(e=>r(e,i)):!!Array.isArray(i)&&(0===e.length||i.every(i=>e.some(e=>r(e,i)))):"object"==typeof i&&null!==i&&Object.entries(e).every(([e,t])=>r(t,i[e])),l=e=>i=>n(e,i);class a{static narrow(e){return new a(i=>n(e,i))}constructor(e){this.NF=void 0,this.NF=e}satisfied(e){return this.NF(e)}build(e){return e}and(e){let i=this.NF,t=e instanceof a?e.NF:e instanceof Function?e:i=>n(e,i);return new a(e=>i(e)&&t(e))}}new a(e=>!0)}},function(e){e.O(0,[2888,9774,179],function(){return e(e.s=13687)}),_N_E=e.O()}]);