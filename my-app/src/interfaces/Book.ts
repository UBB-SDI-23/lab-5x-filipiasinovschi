import { Author } from "./Author"
import { Publisher } from "./Publisher"
import { Buyer } from "./Buyer"

export interface Book {
    id: number
    title: string
    number_of_pages: number
    publish_date: Date
    ibn: number
    author: Author
    publisher: Publisher
    buyers: Buyer[]
    price: number
    quantity:number

}