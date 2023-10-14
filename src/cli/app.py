from transformers import pipeline
from huggingface_hub import hf_hub_download
import click




@click.group()
def cli():
    """ Summarize text from a file or string"""

@cli.command("summarize")
@click.option("--file", type=click.Path(exists=True), help="File to summarize")
@click.option("--text", type=str, help="Text to summarize")
@click.option("--model", default="t5-small", help="Hugging Face model")
@click.option("--tokenizer", default="t5-small", help="Hugging Face tokenizer")
@click.option("--framework", default="tf", help="Options: Tensorflow (tf) or Pytorch (pt)")
def summarize(file, text, model, tokenizer, framework):
    summarizer = pipeline(
                        "summarization",
                        model=model,
                        tokenizer=tokenizer,
                        truncation=True,
                        framework=framework)
    if file:
        with open(file=file, mode="r", encoding="utf-8") as f:
            click.echo(summarizer(f.read()))
    elif text:
        click.echo(summarizer(text))
        
        
@cli.command("sentiment")
@click.option("--file", type=click.Path(exists=True), help="File to summarize")
@click.option("--text", type=str, help="Text to summarize")
@click.option("--model", default="t5-small", help="Hugging Face model")
@click.option("--tokenizer", default="t5-small", help="Hugging Face tokenizer")
@click.option("--framework", default="tf", help="Options: Tensorflow (tf) or Pytorch (pt)")
def sentiment_analysis(file, text, model, tokenizer, framework):
    sentiment = pipeline(
                        "sentiment-analysis",
                        model=model,
                        tokenizer=tokenizer,
                        truncation=True,
                        framework=framework)
    click.echo(sentiment)

if __name__ == "__main__":
    cli()