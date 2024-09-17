import {LRLanguage, LanguageSupport} from "@codemirror/language"
import {parser} from "./parser"

export const eslLanguage = LRLanguage.define({
    name: "esl",
    parser: parser.configure({
        props: []
    }),
    languageData: {
        closeBrackets: {
            brackets: [],
            stringPrefixes: []
        },
        commentTokens: {},
    }
})

export function esl() {
    try {
        return new LanguageSupport(eslLanguage, [])
    } catch (error) {
        console.error(error)
        throw error;
    }
}
