"use client";

import React from "react";
import type { AnalysisResult } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Props {
  result: AnalysisResult;
}

function sentimentColour(label: string) {
  switch (label) {
    case "positive": return "bg-emerald-100 text-emerald-800";
    case "negative": return "bg-red-100 text-red-800";
    case "mixed":    return "bg-amber-100 text-amber-800";
    default:         return "bg-slate-100 text-slate-700";
  }
}

export default function AnalysisResult({ result }: Props) {
  const {
    sentiment,
    entities,
    themes,
    reputation_signals,
    significance_score,
    reasoning,
    sentiment_breakdown,
    contradictions,
    claims,
    source_credibility,
  } = result;

  return (
    <div className="space-y-4 mt-6">

      {/* 1. header — sentiment + significance */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <h2 className="text-xl font-bold text-slate-800">Reputation Analysis</h2>
        <div className="flex items-center gap-3">
          <Badge className={`px-3 py-1 text-sm font-semibold ${sentimentColour(sentiment.label)}`}>
            {sentiment.label.charAt(0).toUpperCase() + sentiment.label.slice(1)}
          </Badge>
          <span className="text-sm text-slate-500">
            Score: <strong>{sentiment.score.toFixed(2)}</strong>
          </span>
          <span className="text-sm text-slate-500">
            Significance: <strong>{(significance_score * 10).toFixed(1)}/10</strong>
          </span>
        </div>
      </div>

      {/* 2. reasoning */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm uppercase tracking-wide text-slate-500">Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-slate-700 leading-relaxed">{reasoning}</p>
        </CardContent>
      </Card>

      {/* 3. themes */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm uppercase tracking-wide text-slate-500">Themes</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {themes.map((theme, i) => (
            <Badge key={i} variant="outline" className="text-sm px-3 py-1">
              {theme}
            </Badge>
          ))}
        </CardContent>
      </Card>

      {/* 4. reputation signals */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm uppercase tracking-wide text-slate-500">Reputation Signals</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* positive */}
          {reputation_signals.positive.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-emerald-600 uppercase mb-2">Positive</p>
              <div className="space-y-2">
                {reputation_signals.positive.map((s, i) => (
                  <div key={i} className="border-l-4 border-emerald-400 pl-3 py-1 bg-emerald-50 rounded-r">
                    <p className="text-sm font-medium text-slate-800">{s.signal}</p>
                    <p className="text-xs italic text-slate-500 mt-1">"{s.evidence}"</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* negative */}
          {reputation_signals.negative.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-red-600 uppercase mb-2">Negative</p>
              <div className="space-y-2">
                {reputation_signals.negative.map((s, i) => (
                  <div key={i} className="border-l-4 border-red-400 pl-3 py-1 bg-red-50 rounded-r">
                    <p className="text-sm font-medium text-slate-800">{s.signal}</p>
                    <p className="text-xs italic text-slate-500 mt-1">"{s.evidence}"</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* neutral */}
          {reputation_signals.neutral.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-slate-500 uppercase mb-2">Neutral</p>
              <div className="space-y-2">
                {reputation_signals.neutral.map((s, i) => (
                  <div key={i} className="border-l-4 border-slate-300 pl-3 py-1 bg-slate-50 rounded-r">
                    <p className="text-sm font-medium text-slate-800">{s.signal}</p>
                    <p className="text-xs italic text-slate-500 mt-1">"{s.evidence}"</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* 5. entities */}
      {entities.length > 0 && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm uppercase tracking-wide text-slate-500">Key Entities</CardTitle>
          </CardHeader>
          <CardContent className="divide-y divide-slate-100">
            {entities.map((e, i) => (
              <div key={i} className="py-2 flex items-start gap-3">
                <Badge variant="outline" className="text-xs mt-0.5 shrink-0">{e.type}</Badge>
                <div>
                  <p className="text-sm font-semibold text-slate-800">{e.name}</p>
                  <p className="text-xs text-slate-500">{e.relationship} — {e.sentiment_context}</p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* 6. sentiment breakdown — optional */}
      {sentiment_breakdown && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm uppercase tracking-wide text-slate-500">Sentiment Breakdown</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {Object.entries(sentiment_breakdown).map(([dim, val]) => (
              <div key={dim} className="flex items-center gap-3">
                <span className="w-40 text-xs text-slate-600 capitalize">{dim.replace(/_/g, " ")}</span>
                <div className="flex-1 bg-slate-100 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${val > 0 ? "bg-emerald-500" : "bg-red-500"}`}
                    style={{ width: `${Math.abs(val) * 100}%` }}
                  />
                </div>
                <span className="text-xs font-medium text-slate-700 w-10 text-right">
                  {val.toFixed(2)}
                </span>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* 7. claims — optional */}
      {claims && claims.length > 0 && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm uppercase tracking-wide text-slate-500">Key Claims</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {claims.map((c, i) => (
              <div key={i} className="border border-slate-200 rounded-lg p-3">
                <div className="flex items-start justify-between gap-2 mb-1">
                  <p className="text-sm font-medium text-slate-800">{c.claim}</p>
                  <Badge variant="outline" className="text-xs shrink-0">{c.claim_type}</Badge>
                </div>
                <p className="text-xs italic text-slate-500">"{c.evidence}"</p>
                <p className="text-xs text-slate-400 mt-1">Significance: {c.significance}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* 8. contradictions — optional */}
      {contradictions && contradictions.length > 0 && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm uppercase tracking-wide text-slate-500">Contradictions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {contradictions.map((c, i) => (
              <div key={i} className="border border-amber-200 bg-amber-50 rounded-lg p-3">
                <p className="text-xs font-semibold text-amber-700 uppercase mb-1">{c.type}</p>
                <p className="text-sm text-slate-700 mb-2">{c.description}</p>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  {Object.entries(c.evidence).map(([frame, quote]) => (
                    <blockquote key={frame} className="italic text-slate-500 border-l-2 border-amber-300 pl-2">
                      "{quote}"
                    </blockquote>
                  ))}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* 9. source credibility — optional */}
      {source_credibility && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm uppercase tracking-wide text-slate-500">Source Credibility</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-start gap-3">
              <Badge className={`shrink-0 ${
                source_credibility.reliability === "high"
                  ? "bg-emerald-100 text-emerald-800"
                  : source_credibility.reliability === "low"
                  ? "bg-red-100 text-red-800"
                  : "bg-amber-100 text-amber-800"
              }`}>
                {String(source_credibility.reliability)} reliability
              </Badge>
              <div>
                <p className="text-sm text-slate-700">{String(source_credibility.bias_assessment)}</p>
                {source_credibility.notes && (
                  <p className="text-xs text-slate-400 mt-1">{String(source_credibility.notes)}</p>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

    </div>
  );
}