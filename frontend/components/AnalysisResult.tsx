"use client";

import type { AnalysisResult } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Props {
  result: AnalysisResult;
}

function sentimentBadgeVariant(label: AnalysisResult["sentiment"]["label"]) {
  switch (label) {
    case "positive":
      return "default";
    case "negative":
      return "destructive";
    case "mixed":
      return "secondary";
    case "neutral":
    default:
      return "outline";
  }
}

function pct(n: number) {
  const v = Math.max(0, Math.min(1, n));
  return `${Math.round(v * 100)}%`;
}

export default function AnalysisResult({ result }: Props) {
  const { sentiment, entities, themes, reputation_signals, significance_score, reasoning } = result;

  return (
    <div className="space-y-4">

      <div className="flex flex-wrap items-center gap-2">
        <h2 className="text-lg font-semibold">Analysis Result</h2>
        <Badge variant={sentimentBadgeVariant(sentiment.label)} className="capitalize">
          {sentiment.label}
        </Badge>
        <span className="text-sm text-muted-foreground">
          score {sentiment.score.toFixed(2)} • confidence {pct(sentiment.confidence)}
        </span>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Significance</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="h-2 w-full rounded bg-muted">
            <div
              className="h-2 rounded bg-foreground"
              style={{ width: pct(significance_score) }}
            />
          </div>
          <p className="text-sm text-muted-foreground">{pct(significance_score)}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Themes</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {themes.map((t) => (
            <Badge key={t} variant="secondary">
              {t}
            </Badge>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Entities</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {entities.length === 0 ? (
            <p className="text-sm text-muted-foreground">No entities detected.</p>
          ) : (
            entities.map((e) => (
              <div key={`${e.name}-${e.type}`} className="rounded-lg border p-3">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-medium">{e.name}</span>
                  <Badge variant="outline" className="capitalize">
                    {e.type}
                  </Badge>
                  <span className="text-xs text-muted-foreground">• {e.relationship}</span>
                </div>
                <p className="mt-2 text-sm text-muted-foreground">{e.sentiment_context}</p>
              </div>
            ))
          )}
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Positive</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {reputation_signals.positive.length === 0 ? (
              <p className="text-sm text-muted-foreground">None</p>
            ) : (
              reputation_signals.positive.map((s, i) => (
                <div key={i} className="text-sm">
                  <p className="font-medium">{s.signal}</p>
                  <p className="text-muted-foreground">{s.evidence}</p>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Negative</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {reputation_signals.negative.length === 0 ? (
              <p className="text-sm text-muted-foreground">None</p>
            ) : (
              reputation_signals.negative.map((s, i) => (
                <div key={i} className="text-sm">
                  <p className="font-medium">{s.signal}</p>
                  <p className="text-muted-foreground">{s.evidence}</p>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Neutral</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {reputation_signals.neutral.length === 0 ? (
              <p className="text-sm text-muted-foreground">None</p>
            ) : (
              reputation_signals.neutral.map((s, i) => (
                <div key={i} className="text-sm">
                  <p className="font-medium">{s.signal}</p>
                  <p className="text-muted-foreground">{s.evidence}</p>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Reasoning</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground whitespace-pre-wrap">{reasoning}</p>
        </CardContent>
      </Card>
    </div>
  );
}