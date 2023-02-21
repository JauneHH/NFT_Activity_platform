let path=[]
var index =0
let k=2
let arr=[1,2,3,4,5]
let len =arr.length
let res = 0
let back =(index)=>{
    if(index>=len){
        return
    }
    if(path.length==k){
        let item_sum=0
        for(let i = 0;i<k;i++){
            item_sum+=path[i]
        }
        if(item_sum%2==0){
            res++
        }
        return
    }
    for(let i = index;i<len;i++){
        path.push(arr[i])
        back(i+1)
        path.pop()
    }
}
back(0)
console.log(res)
