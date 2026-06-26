import { useState } from 'react'
import { ChevronDown, ChevronRight, HelpCircle, MessageCircle } from 'lucide-react'
import { faqCategories, FAQItem } from '../data/faqData'

export function FAQSection() {
  const [openCategory, setOpenCategory] = useState<string | null>(null)
  const [openQuestions, setOpenQuestions] = useState<Set<string>>(new Set())

  const toggleCategory = (id: string) => {
    setOpenCategory((prev) => (prev === id ? null : id))
    setOpenQuestions(new Set())
  }

  const toggleQuestion = (key: string) => {
    setOpenQuestions((prev) => {
      const next = new Set(prev)
      if (next.has(key)) {
        next.delete(key)
      } else {
        next.add(key)
      }
      return next
    })
  }

  return (
    <div className="faq-section">
      <div className="faq-heading">
        <HelpCircle size={16} />
        <span>FAQ</span>
      </div>

      <div className="faq-categories">
        {faqCategories.map((cat) => {
          const isOpen = openCategory === cat.id
          return (
            <div key={cat.id} className="faq-category">
              <button
                className={`faq-category-btn ${isOpen ? 'active' : ''}`}
                onClick={() => toggleCategory(cat.id)}
              >
                <span className="faq-category-title">{cat.title}</span>
                {isOpen ? (
                  <ChevronDown size={16} className="faq-chevron" />
                ) : (
                  <ChevronRight size={16} className="faq-chevron" />
                )}
              </button>

              {isOpen && cat.items.length > 0 && (
                <div className="faq-items">
                  {cat.items.map((item, idx) => (
                    <FAQQuestionItem
                      key={`${cat.id}-${idx}`}
                      item={item}
                      idx={idx}
                      isOpen={openQuestions.has(`${cat.id}-${idx}`)}
                      onToggle={() => toggleQuestion(`${cat.id}-${idx}`)}
                    />
                  ))}
                </div>
              )}

              {isOpen && cat.items.length === 0 && (
                <div className="faq-empty">Вопросы по этой категории появятся позже.</div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

function FAQQuestionItem({
  item,
  idx,
  isOpen,
  onToggle,
}: {
  item: FAQItem
  idx: number
  isOpen: boolean
  onToggle: () => void
}) {
  return (
    <div className={`faq-item ${isOpen ? 'open' : ''}`}>
      <button className="faq-question" onClick={onToggle}>
        <span className="faq-q-num">{idx + 1}</span>
        <span className="faq-q-text">{item.q}</span>
        <ChevronDown size={14} className="faq-q-chevron" />
      </button>
      {isOpen && (
        <div className="faq-answer">
          <div className="faq-answer-accent" />
          <div className="faq-answer-content">
            <MessageCircle size={14} className="faq-a-icon" />
            <div className="faq-a-text">{item.a}</div>
          </div>
        </div>
      )}
    </div>
  )
}
