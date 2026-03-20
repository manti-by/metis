import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import type { Budget, BudgetColumn, CreateItemData, CreateColumnData } from '../types';
import { getBudget, updateBudget, createColumn, deleteColumn, createItem, deleteItem } from '../api';
import './App.css';

function App() {
  const [budget, setBudget] = useState<Budget | null>(null);
  const [plannedAmount, setPlannedAmount] = useState('');
  const [showAddColumn, setShowAddColumn] = useState(false);
  const [newColumnName, setNewColumnName] = useState('');
  const [showAddItem, setShowAddItem] = useState<number | null>(null);
  const [newItem, setNewItem] = useState({ title: '', description: '', cost: '' });

  const loadBudget = useCallback(async () => {
    try {
      const data = await getBudget();
      setBudget(data);
      setPlannedAmount(data.planned_amount.toString());
    } catch (error) {
      console.error('Failed to load budget:', error);
    }
  }, []);

  useEffect(() => {
    loadBudget();
  }, [loadBudget]);

  const handleUpdatePlanned = async () => {
    const amount = parseFloat(plannedAmount);
    if (isNaN(amount)) return;
    try {
      const updated = await updateBudget(amount);
      setBudget(updated);
    } catch (error) {
      console.error('Failed to update planned amount:', error);
    }
  };

  const handleAddColumn = async () => {
    if (!newColumnName.trim() || !budget) return;
    try {
      const data: CreateColumnData = { name: newColumnName, budget_id: budget.id };
      await createColumn(data);
      setNewColumnName('');
      setShowAddColumn(false);
      loadBudget();
    } catch (error) {
      console.error('Failed to add column:', error);
    }
  };

  const handleDeleteColumn = async (columnId: number) => {
    try {
      await deleteColumn(columnId);
      loadBudget();
    } catch (error) {
      console.error('Failed to delete column:', error);
    }
  };

  const handleAddItem = async (columnId: number) => {
    if (!newItem.title.trim() || !newItem.cost) return;
    try {
      const data: CreateItemData = {
        title: newItem.title,
        description: newItem.description || undefined,
        cost: parseFloat(newItem.cost),
        column_id: columnId,
      };
      await createItem(data);
      setNewItem({ title: '', description: '', cost: '' });
      setShowAddItem(null);
      loadBudget();
    } catch (error) {
      console.error('Failed to add item:', error);
    }
  };

  const handleDeleteItem = async (itemId: number) => {
    try {
      await deleteItem(itemId);
      loadBudget();
    } catch (error) {
      console.error('Failed to delete item:', error);
    }
  };

  const totalItemsCost = budget?.columns.reduce(
    (sum, col) => sum + col.items.reduce((s, item) => s + item.cost, 0),
    0
  ) ?? 0;

  if (!budget) {
    return (
      <div className="loading">
        <motion.div
          className="loader"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          Metis
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.6 }}
          transition={{ delay: 0.2, duration: 0.6 }}
        >
          Plan your future expenses
        </motion.p>
      </header>

      <section className="budget-header">
        <div className="planned-section">
          <label htmlFor="planned">Planned to spend</label>
          <div className="input-group">
            <input
              id="planned"
              type="number"
              value={plannedAmount}
              onChange={(e) => setPlannedAmount(e.target.value)}
              onBlur={handleUpdatePlanned}
              onKeyDown={(e) => e.key === 'Enter' && handleUpdatePlanned()}
            />
            <span className="currency">$</span>
          </div>
        </div>
        <div className="total-section">
          <span className="total-label">Total items cost</span>
          <motion.span
            className={`total-value ${totalItemsCost > budget.planned_amount ? 'over-budget' : ''}`}
            animate={{ scale: [1, 1.05, 1] }}
            transition={{ duration: 0.3 }}
            key={totalItemsCost}
          >
            ${totalItemsCost.toFixed(2)}
          </motion.span>
        </div>
        <div className="tools-section">
          <motion.button
            className="tool-btn"
            onClick={() => setShowAddColumn(!showAddColumn)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            + Add Column
          </motion.button>
        </div>
      </section>

      <AnimatePresence>
        {showAddColumn && (
          <motion.div
            className="add-column-form"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <input
              type="text"
              placeholder="Column name"
              value={newColumnName}
              onChange={(e) => setNewColumnName(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAddColumn()}
              autoFocus
            />
            <button onClick={handleAddColumn}>Add</button>
            <button onClick={() => { setShowAddColumn(false); setNewColumnName(''); }}>Cancel</button>
          </motion.div>
        )}
      </AnimatePresence>

      <main className="columns-container">
        <AnimatePresence mode="popLayout">
          {budget.columns.map((column, index) => (
            <motion.div
              key={column.id}
              className="column"
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ delay: index * 0.1, duration: 0.4 }}
            >
              <div className="column-header">
                <h3>{column.name}</h3>
                <button
                  className="delete-col-btn"
                  onClick={() => handleDeleteColumn(column.id)}
                  title="Delete column"
                >
                  ×
                </button>
              </div>
              <div className="items-list">
                <AnimatePresence mode="popLayout">
                  {column.items.map((item) => (
                    <motion.div
                      key={item.id}
                      className="item-card"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      layout
                    >
                      <div className="item-header">
                        <span className="item-title">{item.title}</span>
                        <span className="item-cost">${item.cost.toFixed(2)}</span>
                      </div>
                      {item.description && (
                        <p className="item-description">{item.description}</p>
                      )}
                      <button
                        className="delete-item-btn"
                        onClick={() => handleDeleteItem(item.id)}
                      >
                        Delete
                      </button>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
              <div className="add-item-section">
                <AnimatePresence mode="wait">
                  {showAddItem === column.id ? (
                    <motion.div
                      className="add-item-form"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                    >
                      <input
                        type="text"
                        placeholder="Title"
                        value={newItem.title}
                        onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
                        autoFocus
                      />
                      <input
                        type="text"
                        placeholder="Description (optional)"
                        value={newItem.description}
                        onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
                      />
                      <input
                        type="number"
                        placeholder="Cost"
                        value={newItem.cost}
                        onChange={(e) => setNewItem({ ...newItem, cost: e.target.value })}
                      />
                      <div className="form-actions">
                        <button onClick={() => handleAddItem(column.id)}>Add</button>
                        <button onClick={() => { setShowAddItem(null); setNewItem({ title: '', description: '', cost: '' }); }}>
                          Cancel
                        </button>
                      </div>
                    </motion.div>
                  ) : (
                    <motion.button
                      className="add-item-btn"
                      onClick={() => setShowAddItem(column.id)}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      + Add Item
                    </motion.button>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
