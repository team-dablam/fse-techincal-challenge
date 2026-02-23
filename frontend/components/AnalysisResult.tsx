"use client";

import type { AnalysisResult } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "./ui/card";

interface Props {
  result: AnalysisResult;
}

export default function AnalysisResult({ result }: Props) {
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold">Analysis Result</h2>
      <Card>
        <CardHeader>
          <CardTitle>Sentiment</CardTitle>
          <CardDescription>
            Label: {result.sentiment.label}, Score: {result.sentiment.score}, Confidence:{" "}
            {result.sentiment.confidence}
          </CardDescription>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Entities</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {result.entities.map((e, idx) => (
            <Card key={idx} className="border-l-4 border-blue-400 bg-blue-50">
              <CardHeader>
                <CardTitle>{e.name} · {e.type}</CardTitle>
                <CardDescription>Relationship: {e.relationship}</CardDescription>
              </CardHeader>
              <CardContent>{e.sentiment_context}</CardContent>
            </Card>
          ))}
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Themes</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-disc list-inside space-y-1">
            {result.themes.map((theme, idx) => (
              <li key={idx}>{theme}</li>
            ))}
          </ul>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Reputation Signals</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h3 className="font-semibold mb-2">Positive</h3>
            {result.reputation_signals.positive.map((s, idx) => (
              <Card key={idx} className="border-l-4 border-green-500 bg-green-50 mb-2">
                <CardHeader>
                  <CardTitle>{s.signal}</CardTitle>
                </CardHeader>
                <CardContent>{s.evidence}</CardContent>
              </Card>
            ))}
          </div>
          <div>
            <h3 className="font-semibold mb-2">Negative</h3>
            {result.reputation_signals.negative.map((s, idx) => (
              <Card key={idx} className="border-l-4 border-red-500 bg-red-50 mb-2">
                <CardHeader>
                  <CardTitle>{s.signal}</CardTitle>
                </CardHeader>
                <CardContent>{s.evidence}</CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Significance Score</CardTitle>
        </CardHeader>
        <CardContent>{result.significance_score}</CardContent>

        <CardHeader className="mt-4">
          <CardTitle>Reasoning</CardTitle>
        </CardHeader>
        <CardContent>{result.reasoning}</CardContent>
      </Card>
    </div>
  );
}
