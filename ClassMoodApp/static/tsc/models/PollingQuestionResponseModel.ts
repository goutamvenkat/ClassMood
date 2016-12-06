//Data model for polling question responses
module ClassMoodApp {
    export class PollingQuestionResponseModel {
        A: number;
        B: number;
        C: number;
        D: number;
        correct_answer: string;
        num_responses: number;
        polled: boolean;
    }
}