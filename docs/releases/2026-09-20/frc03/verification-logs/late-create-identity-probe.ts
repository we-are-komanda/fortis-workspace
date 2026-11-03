import assert from "node:assert/strict";
import {createWorkspaceDefenseProject} from "../../../../../frontend/src/shared/lib/defense-project.ts";
import {useDefenseProjectStore as projects} from "../../../../../frontend/src/shared/lib/use-defense-project-store.ts";
import {useDefenseVariantsStore as variants} from "../../../../../frontend/src/modules/drone-defense/domain/use-defense-variants-store.ts";
import {setAuthenticatedIdentity} from "../../../../../frontend/src/shared/lib/session-state.ts";
import "../../../../../frontend/src/shared/lib/identity.ts";
async function main(){
 setAuthenticatedIdentity("A");
 const old={...createWorkspaceDefenseProject(),projectId:"P",enterpriseId:"E",version:1,source:"backend" as const};
 projects.getState().acceptServerProject(old);variants.setState({activeVariantId:"P"});
 const proposal={...createWorkspaceDefenseProject(),enterpriseId:"E",projectName:"Created"};
 let release!:()=>void,arrived!:()=>void;
 const pending=new Promise<void>(r=>release=r),started=new Promise<void>(r=>arrived=r);
 const original=globalThis.fetch;
 globalThis.fetch=async(_input,init)=>{if(init?.method==="POST")return new Response(JSON.stringify({projectId:"Created",enterpriseId:"E",version:1,name:"Created"}),{status:200});arrived();await pending;return new Response(JSON.stringify({items:[],totalItems:0}),{status:200})};
 try{const operation=variants.getState().saveAsNewVariant("Created",proposal);await started;setAuthenticatedIdentity("B");release();const result=await operation;console.log(JSON.stringify({currentIdentity:projects.getState().identityId,result}));assert.equal(result,null,"stale operation cannot authorize caller navigation after identity change");}
 finally{globalThis.fetch=original;release?.();}
}
void main();
