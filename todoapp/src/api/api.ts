import axios from 'axios'
export const baseUrl = 'http://127.0.0.1:3000'
export const http = () => {
    return axios
}
export const login = (data: any): Promise<any> => {
    return new Promise((reslove: Function, reject: Function) => {
        axios({
            url: baseUrl + '/data/login',
            method: 'post',
            headers: {
                'JwtToken': localStorage.getItem('token')
            },
            data
        }).then(res => {
            if (res.status === 400) {
                localStorage.removeItem('token')
                reject(res)
            } else if (res.status === 200) {
                reslove(res.data)
            } else (
                reject(res)
            )
        }).catch(err => {
            reject(err)
        })
    })


}
