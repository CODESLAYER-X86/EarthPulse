import React, { useEffect, useState } from 'react';
import { X, FileText, ChevronRight } from 'lucide-react';
import { ReportItem } from '../types';

interface ReportsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ReportsModal: React.FC<ReportsModalProps> = ({ isOpen, onClose }) => {
  const [reports, setReports] = useState<ReportItem[]>([]);
  const [selectedReportId, setSelectedReportId] = useState<string>('');
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (!isOpen) return;
    fetch('/api/reports')
      .then((res) => res.json())
      .then((data: ReportItem[]) => {
        setReports(data);
        if (data.length > 0 && !selectedReportId) {
          setSelectedReportId(data[0].id);
        }
      })
      .catch(console.error);
  }, [isOpen]);

  useEffect(() => {
    if (!selectedReportId) return;
    setLoading(true);
    fetch(`/api/reports/${selectedReportId}`)
      .then((res) => res.json())
      .then((data) => {
        setContent(data.content);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [selectedReportId]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 flex items-center justify-center p-6">
      <div className="bg-[#111827] border border-gray-800 rounded-lg w-full max-w-4xl h-[80vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Modal Header */}
        <div className="h-14 border-b border-gray-800 px-6 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-blue-400" />
            <h2 className="text-base font-semibold text-white">Scientific Validation & Methodology Reports</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-gray-800 text-gray-400 hover:text-white transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 flex overflow-hidden">
          {/* Reports Sidebar */}
          <div className="w-64 border-r border-gray-800 bg-[#0b0f19]/60 overflow-y-auto p-3 space-y-1">
            {reports.map((rep) => (
              <button
                key={rep.id}
                onClick={() => setSelectedReportId(rep.id)}
                className={`w-full text-left p-2.5 rounded text-xs transition flex items-center justify-between ${
                  selectedReportId === rep.id
                    ? 'bg-blue-600/20 text-blue-300 border border-blue-500/40 font-medium'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
                }`}
              >
                <span className="truncate">{rep.title}</span>
                <ChevronRight className="w-3.5 h-3.5 flex-shrink-0 ml-1 text-gray-500" />
              </button>
            ))}
          </div>

          {/* Report Viewer */}
          <div className="flex-1 overflow-y-auto p-6 bg-[#0f172a]">
            {loading ? (
              <div className="text-xs text-gray-400">Loading document...</div>
            ) : (
              <pre className="text-xs text-gray-200 font-mono whitespace-pre-wrap leading-relaxed select-text">
                {content}
              </pre>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
