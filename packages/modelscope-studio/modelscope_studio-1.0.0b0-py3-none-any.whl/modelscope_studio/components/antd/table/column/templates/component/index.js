function z(s) {
  const {
    gradio: t,
    _internal: o,
    ...n
  } = s;
  return Object.keys(o).reduce((e, r) => {
    const l = r.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], c = u.split("_"), f = (...d) => {
        const p = d.map((a) => d && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
          type: a.type,
          detail: a.detail,
          timestamp: a.timeStamp,
          clientX: a.clientX,
          clientY: a.clientY,
          targetId: a.target.id,
          targetClassName: a.target.className,
          altKey: a.altKey,
          ctrlKey: a.ctrlKey,
          shiftKey: a.shiftKey,
          metaKey: a.metaKey
        } : a);
        return t.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (c.length > 1) {
        let d = {
          ...n.props[c[0]] || {}
        };
        e[c[0]] = d;
        for (let a = 1; a < c.length - 1; a++) {
          const h = {
            ...n.props[c[a]] || {}
          };
          d[c[a]] = h, d = h;
        }
        const p = c[c.length - 1];
        return d[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = f, e;
      }
      const _ = c[0];
      e[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return e;
  }, {});
}
function P() {
}
function H(s, t) {
  return s != s ? t == t : s !== t || s && typeof s == "object" || typeof s == "function";
}
function R(s, ...t) {
  if (s == null) {
    for (const n of t)
      n(void 0);
    return P;
  }
  const o = s.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function g(s) {
  let t;
  return R(s, (o) => t = o)(), t;
}
const C = [];
function y(s, t = P) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function e(u) {
    if (H(s, u) && (s = u, o)) {
      const c = !C.length;
      for (const f of n)
        f[1](), C.push(f, s);
      if (c) {
        for (let f = 0; f < C.length; f += 2)
          C[f][0](C[f + 1]);
        C.length = 0;
      }
    }
  }
  function r(u) {
    e(u(s));
  }
  function l(u, c = P) {
    const f = [u, c];
    return n.add(f), n.size === 1 && (o = t(e, r) || P), u(s), () => {
      n.delete(f), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: e,
    update: r,
    subscribe: l
  };
}
const {
  getContext: T,
  setContext: k
} = window.__gradio__svelte__internal, X = "$$ms-gr-antd-slots-key";
function Y() {
  const s = y({});
  return k(X, s);
}
const L = "$$ms-gr-antd-render-slot-context-key";
function Z() {
  const s = k(L, y({}));
  return (t, o) => {
    s.update((n) => typeof o == "function" ? {
      ...n,
      [t]: o(n[t])
    } : {
      ...n,
      [t]: o
    });
  };
}
const B = "$$ms-gr-antd-context-key";
function G(s) {
  var u;
  if (!Reflect.has(s, "as_item") || !Reflect.has(s, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = A(), o = W({
    slot: void 0,
    index: s._internal.index,
    subIndex: s._internal.subIndex
  });
  t && t.subscribe((c) => {
    o.slotKey.set(c);
  }), J();
  const n = T(B), e = ((u = g(n)) == null ? void 0 : u.as_item) || s.as_item, r = n ? e ? g(n)[e] : g(n) : {}, l = y({
    ...s,
    ...r
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: f
    } = g(l);
    f && (c = c[f]), l.update((_) => ({
      ..._,
      ...c
    }));
  }), [l, (c) => {
    const f = c.as_item ? g(n)[c.as_item] : g(n);
    return l.set({
      ...c,
      ...f
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const U = "$$ms-gr-antd-slot-key";
function J() {
  k(U, y(void 0));
}
function A() {
  return T(U);
}
const Q = "$$ms-gr-antd-component-slot-context-key";
function W({
  slot: s,
  index: t,
  subIndex: o
}) {
  return k(Q, {
    slotKey: y(s),
    slotIndex: y(t),
    subSlotIndex: y(o)
  });
}
function m(s) {
  try {
    return typeof s == "string" ? new Function(`return (...args) => (${s})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function $(s) {
  return s && s.__esModule && Object.prototype.hasOwnProperty.call(s, "default") ? s.default : s;
}
var D = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(s) {
  (function() {
    var t = {}.hasOwnProperty;
    function o() {
      for (var r = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (r = e(r, n(u)));
      }
      return r;
    }
    function n(r) {
      if (typeof r == "string" || typeof r == "number")
        return r;
      if (typeof r != "object")
        return "";
      if (Array.isArray(r))
        return o.apply(null, r);
      if (r.toString !== Object.prototype.toString && !r.toString.toString().includes("[native code]"))
        return r.toString();
      var l = "";
      for (var u in r)
        t.call(r, u) && r[u] && (l = e(l, u));
      return l;
    }
    function e(r, l) {
      return l ? r ? r + " " + l : r + l : r;
    }
    s.exports ? (o.default = o, s.exports = o) : window.classNames = o;
  })();
})(D);
var tt = D.exports;
const et = /* @__PURE__ */ $(tt), {
  getContext: nt,
  setContext: st
} = window.__gradio__svelte__internal;
function ot(s) {
  const t = `$$ms-gr-antd-${s}-context-key`;
  function o(e = ["default"]) {
    const r = e.reduce((l, u) => (l[u] = y([]), l), {});
    return st(t, {
      itemsMap: r,
      allowedSlots: e
    }), r;
  }
  function n() {
    const {
      itemsMap: e,
      allowedSlots: r
    } = nt(t);
    return function(l, u, c) {
      e && (l ? e[l].update((f) => {
        const _ = [...f];
        return r.includes(l) ? _[u] = c : _[u] = void 0, _;
      }) : r.includes("default") && e.default.update((f) => {
        const _ = [...f];
        return _[u] = c, _;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: n
  };
}
const {
  getItems: Ct,
  getSetItemFn: rt
} = ot("table-column"), {
  SvelteComponent: it,
  check_outros: lt,
  component_subscribe: K,
  create_slot: ct,
  detach: ut,
  empty: ft,
  flush: b,
  get_all_dirty_from_scope: at,
  get_slot_changes: _t,
  group_outros: mt,
  init: dt,
  insert: pt,
  safe_not_equal: bt,
  transition_in: j,
  transition_out: F,
  update_slot_base: yt
} = window.__gradio__svelte__internal;
function q(s) {
  let t;
  const o = (
    /*#slots*/
    s[18].default
  ), n = ct(
    o,
    s,
    /*$$scope*/
    s[17],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(e, r) {
      n && n.m(e, r), t = !0;
    },
    p(e, r) {
      n && n.p && (!t || r & /*$$scope*/
      131072) && yt(
        n,
        o,
        e,
        /*$$scope*/
        e[17],
        t ? _t(
          o,
          /*$$scope*/
          e[17],
          r,
          null
        ) : at(
          /*$$scope*/
          e[17]
        ),
        null
      );
    },
    i(e) {
      t || (j(n, e), t = !0);
    },
    o(e) {
      F(n, e), t = !1;
    },
    d(e) {
      n && n.d(e);
    }
  };
}
function ht(s) {
  let t, o, n = (
    /*$mergedProps*/
    s[0].visible && q(s)
  );
  return {
    c() {
      n && n.c(), t = ft();
    },
    m(e, r) {
      n && n.m(e, r), pt(e, t, r), o = !0;
    },
    p(e, [r]) {
      /*$mergedProps*/
      e[0].visible ? n ? (n.p(e, r), r & /*$mergedProps*/
      1 && j(n, 1)) : (n = q(e), n.c(), j(n, 1), n.m(t.parentNode, t)) : n && (mt(), F(n, 1, 1, () => {
        n = null;
      }), lt());
    },
    i(e) {
      o || (j(n), o = !0);
    },
    o(e) {
      F(n), o = !1;
    },
    d(e) {
      e && ut(t), n && n.d(e);
    }
  };
}
function gt(s, t, o) {
  let n, e, r, l, {
    $$slots: u = {},
    $$scope: c
  } = t, {
    gradio: f
  } = t, {
    props: _ = {}
  } = t;
  const d = y(_);
  K(s, d, (i) => o(16, l = i));
  let {
    _internal: p = {}
  } = t, {
    as_item: a
  } = t, {
    built_in_column: h
  } = t, {
    visible: S = !0
  } = t, {
    elem_id: x = ""
  } = t, {
    elem_classes: w = []
  } = t, {
    elem_style: I = {}
  } = t;
  const O = A();
  K(s, O, (i) => o(15, r = i));
  const [E, M] = G({
    gradio: f,
    props: l,
    _internal: p,
    visible: S,
    elem_id: x,
    elem_classes: w,
    elem_style: I,
    as_item: a
  });
  K(s, E, (i) => o(0, e = i));
  const N = Y();
  K(s, N, (i) => o(14, n = i));
  const V = rt(), v = Z();
  return s.$$set = (i) => {
    "gradio" in i && o(5, f = i.gradio), "props" in i && o(6, _ = i.props), "_internal" in i && o(7, p = i._internal), "as_item" in i && o(8, a = i.as_item), "built_in_column" in i && o(9, h = i.built_in_column), "visible" in i && o(10, S = i.visible), "elem_id" in i && o(11, x = i.elem_id), "elem_classes" in i && o(12, w = i.elem_classes), "elem_style" in i && o(13, I = i.elem_style), "$$scope" in i && o(17, c = i.$$scope);
  }, s.$$.update = () => {
    if (s.$$.dirty & /*props*/
    64 && d.update((i) => ({
      ...i,
      ..._
    })), s.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    81312 && M({
      gradio: f,
      props: l,
      _internal: p,
      visible: S,
      elem_id: x,
      elem_classes: w,
      elem_style: I,
      as_item: a
    }), s.$$.dirty & /*$mergedProps, $slotKey, built_in_column, $slots*/
    49665) {
      const i = e.props.showSorterTooltip;
      V(r, e._internal.index || 0, h || {
        props: {
          style: e.elem_style,
          className: et(e.elem_classes, "ms-gr-antd-table-column"),
          id: e.elem_id,
          ...e.props,
          ...z(e),
          render: m(e.props.render),
          filterIcon: m(e.props.filterIcon),
          filterDropdown: m(e.props.filterDropdown),
          showSorterTooltip: n["showSorterTooltip.title"] || typeof i == "object" ? {
            afterOpenChange: m(typeof i == "object" ? i.afterOpenChange : void 0),
            getPopupContainer: m(typeof i == "object" ? i.getPopupContainer : void 0)
          } : i,
          sorter: typeof e.props.sorter == "object" ? {
            ...e.props.sorter,
            compare: m(e.props.sorter.compare) || e.props.sorter.compare
          } : m(e.props.sorter) || e.props.sorter,
          filterSearch: m(e.props.filterSearch) || e.props.filterSearch,
          shouldCellUpdate: m(e.props.shouldCellUpdate),
          onCell: m(e.props.onCell),
          onFilter: m(e.props.onFilter),
          onHeaderCell: m(e.props.onHeaderCell)
        },
        slots: {
          ...n,
          filterIcon: {
            el: n.filterIcon,
            callback: v
          },
          sortIcon: {
            el: n.sortIcon,
            callback: v
          },
          title: {
            el: n.title,
            callback: v
          }
        }
      });
    }
  }, [e, d, O, E, N, f, _, p, a, h, S, x, w, I, n, r, l, c, u];
}
class St extends it {
  constructor(t) {
    super(), dt(this, t, gt, ht, bt, {
      gradio: 5,
      props: 6,
      _internal: 7,
      as_item: 8,
      built_in_column: 9,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), b();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(t) {
    this.$$set({
      props: t
    }), b();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), b();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), b();
  }
  get built_in_column() {
    return this.$$.ctx[9];
  }
  set built_in_column(t) {
    this.$$set({
      built_in_column: t
    }), b();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), b();
  }
}
export {
  St as default
};
